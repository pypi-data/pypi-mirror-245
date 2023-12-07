# -*- coding: utf-8 -*-
# This file is part of the investment-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.tests.test_tryton import with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from decimal import Decimal
from datetime import time, date, datetime
from unittest.mock import MagicMock
from requests import Response
import requests


class SourceTestCase(object):
    """ test online source
    """
    @with_transaction()
    def test_waitlist_source_request(self):
        """ create source, call server
        """
        pool = Pool()
        OSource = pool.get('investment.source')
        Asset = pool.get('investment.asset')
        Product = pool.get('product.product')

        company = self.prep_asset_company()
        with Transaction().set_context({'company': company.id}):
            osource, = OSource.create([{
                'name': 'Source 1',
                'url': 'https://foo.bar/${isin}/${nsin}/${symbol}',
                'rgxdate': 'Course Date (\\d+.\\d+.\\d+) Today',
                'rgxdatefmt': '%d.%m.%Y',
                'rgxrate': 'High (\\d+,\\d+) EUR',
                'rgxdecimal': ',',
                }])
            self.assertEqual(osource.rec_name, 'Source 1')

            product = self.prep_asset_product(
                name='Product 1',
                description='some asset')

            Product.write(*[
                [product],
                {
                    'identifiers': [('create', [{
                        'type': 'wkn',
                        'code': '965515',
                        }, {
                        'type': 'secsymb',
                        'code': '1472977',
                        }, {
                        'type': 'isin',
                        'code': 'XC0009655157',
                        }, ])],
                }])

            asset = self.prep_asset_item(company=company, product=product)

            Asset.write(*[
                [asset],
                {
                    'updtsources': [('add', [osource.id])],
                }])

            with Transaction().set_context({
                    'qdate': date(2022, 10, 1),     # saturday
                    'qdatetime': datetime(2022, 10, 2, 10, 0, 0)}):
                asset2, = Asset.browse([asset])
                self.assertEqual(asset2.wkn, '965515')
                self.assertEqual(asset2.isin, 'XC0009655157')
                self.assertEqual(asset2.secsymb, '1472977')
                self.assertEqual(asset2.updttime, time(14, 0))
                self.assertEqual(len(asset2.updtsources), 1)
                self.assertEqual(asset2.updtsources[0].rec_name, 'Source 1')
                self.assertEqual(asset2.updtdays, 'work')
                self.assertEqual(
                    asset2.nextupdate, datetime(2022, 10, 3, 14, 0))
                self.assertEqual(len(asset.rates), 0)

                # fake server-response
                resp1 = Response()
                resp1._content = """<html><body>Response from finance-server
Course Date 14.08.2022 Today
High 34,87 EUR
</body></html>""".encode('utf8')
                resp1.status_code = 200
                resp1.reason = 'OK'
                requests.get = MagicMock(return_value=resp1)

                OSource.update_rate(asset)
                self.assertEqual(len(asset.rates), 1)
                self.assertEqual(asset.rates[0].date, date(2022, 8, 14))
                self.assertEqual(asset.rates[0].rate, Decimal('34.87'))

    @with_transaction()
    def test_waitlist_source_check_regex(self):
        """ create source, check convert
        """
        pool = Pool()
        OSource = pool.get('investment.source')

        osource, = OSource.create([{
            'name': 'Source 1',
            'rgxdate': 'Course Date (\\d+.\\d+.\\d+) Today',
            'rgxdatefmt': '%d.%m.%Y',
            'rgxrate': 'High (\\d+,\\d+) EUR',
            'rgxdecimal': ',',
            }])
        self.assertEqual(osource.rec_name, 'Source 1')
        self.assertEqual(osource.get_regex_result(
            'The Course Date 14.03.2022 Today, High 13,43 EUR',
            'rgxdate'
            ), date(2022, 3, 14))

        self.assertEqual(osource.get_regex_result(
            'The Course Date 14.03.2022 Today, High 13,43 EUR',
            'rgxrate'
            ), Decimal('13.43'))

        # iso-date
        OSource.write(*[
            [osource],
            {
                'rgxdate': 'Course Date (\\d+-\\d+-\\d+) Today',
                'rgxdatefmt': '%Y-%m-%d',
            }])
        self.assertEqual(osource.get_regex_result(
            'The Course Date 2022-03-14 Today, High 13,43 EUR',
            'rgxdate'
            ), date(2022, 3, 14))


# end SourceTestCase
