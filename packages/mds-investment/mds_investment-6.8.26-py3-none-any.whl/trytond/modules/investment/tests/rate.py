# -*- coding: utf-8 -*-
# This file is part of the investment-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.tests.test_tryton import with_transaction
from trytond.transaction import Transaction
from trytond.pool import Pool
from decimal import Decimal
from datetime import date


class RateTestCase(object):
    """ test rate
    """
    @with_transaction()
    def test_rate_create(self):
        """ create rate
        """
        Asset = Pool().get('investment.asset')

        company = self.prep_asset_company()
        with Transaction().set_context({'company': company.id}):
            product = self.prep_asset_product(
                name='Product 1',
                description='some asset')

            asset = self.prep_asset_item(company=company, product=product)

            Asset.write(*[
                [asset],
                {
                    'rates': [('create', [{
                        'date': date(2022, 5, 1),
                        'rate': Decimal('2.5'),
                        }, {
                        'date': date(2022, 5, 2),
                        'rate': Decimal('2.8'),
                        }])],
                }])
            self.assertEqual(len(asset.rates), 2)
            self.assertEqual(asset.rates[0].date, date(2022, 5, 2))
            self.assertEqual(asset.rates[0].rate, Decimal('2.8'))
            self.assertEqual(asset.rates[0].uom.rec_name, 'Unit')
            self.assertEqual(asset.rates[0].asset_digits, 4)
            self.assertEqual(asset.rates[0].currency.rec_name, 'usd')
            self.assertEqual(asset.rates[0].symbol, '%')
            self.assertEqual(asset.change_symbol.symbol, '%')

# end RateTestCase
