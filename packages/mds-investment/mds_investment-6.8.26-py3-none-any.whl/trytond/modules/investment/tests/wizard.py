# -*- coding: utf-8 -*-
# This file is part of the investment-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.tests.test_tryton import with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from decimal import Decimal
from datetime import date


class WizardTestCase(object):
    """ test import wizard
    """
    @with_transaction()
    def test_wiz_run_import(self):
        """ run import wizard
        """
        pool = Pool()
        ImportWiz = pool.get('investment.imp_wiz', type='wizard')

        company = self.prep_asset_company()
        with Transaction().set_context({'company': company.id}):
            product = self.prep_asset_product(
                name='Product 1',
                description='some asset')

            asset = self.prep_asset_item(company=company, product=product)
            self.assertEqual(len(asset.rates), 0)

            with Transaction().set_context({
                    'active_id': asset.id,
                    'active_model': 'investment.asset'}):
                (sess_id, start_state, end_state) = ImportWiz.create()
                w_obj = ImportWiz(sess_id)
                self.assertEqual(start_state, 'start')
                self.assertEqual(end_state, 'end')

                # run start
                result = ImportWiz.execute(sess_id, {}, start_state)
                self.assertEqual(list(result.keys()), ['view'])

                self.assertEqual(result['view']['defaults']['asset'], asset.id)
                self.assertEqual(result['view']['defaults']['dec_divider'], ',')
                self.assertEqual(
                    result['view']['defaults']['date_fmt'],
                    '%d.%m.%Y')
                self.assertEqual(
                    result['view']['defaults']['field_delimiter'],
                    ';')

                w_obj.start.asset = asset
                w_obj.start.dec_divider = ','
                w_obj.start.date_fmt = '%d.%m.%Y'
                w_obj.start.field_delimiter = ';'

                result = ImportWiz.execute(sess_id, {'start': {
                    'asset': asset.id,
                    'dec_divider': ',',
                    'date_fmt': '%d.%m.%Y',
                    'field_delimiter': ';',
                    'file_': b'"date";"rate"\n"03.05.2022";"23,56"\n' +
                    b'"05.05.2022";"24,22"\n"06.05.2022";"25,43"',
                    }}, 'importf')
                self.assertEqual(list(result.keys()), [])
                # finish wizard
                ImportWiz.delete(sess_id)

            self.assertEqual(len(asset.rates), 3)
            self.assertEqual(asset.rates[0].date, date(2022, 5, 6))
            self.assertEqual(asset.rates[0].rate, Decimal('25.43'))
            self.assertEqual(asset.rates[1].date, date(2022, 5, 5))
            self.assertEqual(asset.rates[1].rate, Decimal('24.22'))
            self.assertEqual(asset.rates[2].date, date(2022, 5, 3))
            self.assertEqual(asset.rates[2].rate, Decimal('23.56'))

# end WizardTestCase
