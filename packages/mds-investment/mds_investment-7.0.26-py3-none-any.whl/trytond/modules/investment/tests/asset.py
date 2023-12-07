# -*- coding: utf-8 -*-
# This file is part of the investment-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.tests.test_tryton import with_transaction
from trytond.pool import Pool
from trytond.modules.company.tests import create_company
from trytond.transaction import Transaction
from trytond.exceptions import UserError
from decimal import Decimal
from datetime import time, date, datetime


class AssetTestCase(object):
    """ test asset
    """
    def prep_asset_company(self):
        """ get/create company
        """
        Company = Pool().get('company.company')

        company = Company.search([])
        if len(company) > 0:
            company = company[0]
        else:
            company = create_company(name='m-ds')
        return company

    def prep_asset_product(
            self, name='Product 1', description=None, unit='u',
            unit_name='Units'):
        """ create product
        """
        pool = Pool()
        Product = pool.get('product.template')
        Uom = pool.get('product.uom')

        uom, = Uom.search([('symbol', '=', unit)])
        prod_templ, = Product.create([{
            'name': name,
            'type': 'assets',
            'list_price': Decimal('1.0'),
            'default_uom': uom.id,
            'products': [('create', [{
                'description': description,
                }])],
            }])
        self.assertEqual(prod_templ.default_uom.symbol, unit)
        self.assertEqual(prod_templ.products[0].description, description)
        return prod_templ.products[0]

    def prep_asset_item(self, company, product):
        """ create asset
        """
        pool = Pool()
        Asset = pool.get('investment.asset')

        asset, = Asset.create([{
            'company': company.id,
            'product': product.id,
            'currency': company.currency.id,
            'currency_digits': 4,
            'uom': product.default_uom.id,
            }])
        self.assertEqual(asset.rec_name, '%s | - usd/%s | -' % (
                product.rec_name,
                asset.uom.symbol,
                ))
        self.assertEqual(asset.currency.rec_name, 'usd')
        self.assertEqual(asset.currency_digits, 4)
        self.assertEqual(asset.product.rec_name, product.name)
        self.assertEqual(asset.uom.symbol, product.default_uom.symbol)
        return asset

    @with_transaction()
    def test_asset_create(self):
        """ create asset
        """
        Asset = Pool().get('investment.asset')

        company = self.prep_asset_company()
        with Transaction().set_context({'company': company.id}):
            product = self.prep_asset_product(
                name='Product 1',
                description='some asset')

            asset = self.prep_asset_item(
                company=company,
                product=product)
            self.assertEqual(asset.symbol, 'usd/u')
            self.assertEqual(asset.asset_symbol.symbol, 'usd/u')

            # check ranges
            Asset.write(*[
                [asset],
                {
                    'currency_digits': 1,
                }])
            self.assertRaisesRegex(
                UserError,
                'ss',
                Asset.write,
                *[[asset], {
                    'currency_digits': -1,
                }])

    @with_transaction()
    def test_asset_rec_name(self):
        """ create asset
        """
        Asset = Pool().get('investment.asset')

        company = self.prep_asset_company()
        with Transaction().set_context({'company': company.id}):
            product = self.prep_asset_product(
                name='Product 1',
                description='some asset')

            asset = self.prep_asset_item(
                company=company,
                product=product)

            self.assertEqual(asset.rec_name, 'Product 1 | - usd/u | -')

            Asset.write(*[
                [asset],
                {
                    'rates': [('create', [{
                        'date': date(2022, 5, 15),
                        'rate': Decimal('2.45'),
                        }])],
                }])
            self.assertEqual(
                asset.rec_name,
                'Product 1 | 2.4500 usd/u | 05/15/2022')
            self.assertEqual(
                Asset.search_count([('name', '=', 'Product 1')]),
                1)

    @with_transaction()
    def test_asset_order_and_search_rate_and_date(self):
        """ create asset, check order of rate + date
        """
        Asset = Pool().get('investment.asset')

        company = self.prep_asset_company()
        with Transaction().set_context({'company': company.id}):
            product1 = self.prep_asset_product(
                name='Product 1',
                description='some asset')
            product2 = self.prep_asset_product(
                name='Product 2',
                description='some asset')

            asset1 = self.prep_asset_item(company=company, product=product1)
            asset2 = self.prep_asset_item(company=company, product=product2)

            Asset.write(*[
                [asset1],
                {
                    'rates': [('create', [{
                        'date': date(2022, 5, 18),
                        'rate': Decimal('3.5'),
                        }, {
                        'date': date(2022, 5, 15),
                        'rate': Decimal('2.45'),
                        }])],
                },
                [asset2],
                {
                    'rates': [('create', [{
                        'date': date(2022, 5, 17),
                        'rate': Decimal('2.6'),
                        }, {
                        'date': date(2022, 5, 14),
                        'rate': Decimal('2.4'),
                        }])],
                },
                ])
            self.assertEqual(
                asset1.rec_name,
                'Product 1 | 3.5000 usd/u | 05/18/2022')
            self.assertEqual(
                asset2.rec_name,
                'Product 2 | 2.6000 usd/u | 05/17/2022')

            assets = Asset.search([], order=[('date', 'ASC')])
            self.assertEqual(len(assets), 2)
            self.assertEqual(assets[0].date, date(2022, 5, 17))
            self.assertEqual(assets[1].date, date(2022, 5, 18))

            assets = Asset.search([], order=[('date', 'DESC')])
            self.assertEqual(len(assets), 2)
            self.assertEqual(assets[0].date, date(2022, 5, 18))
            self.assertEqual(assets[1].date, date(2022, 5, 17))

            assets = Asset.search([], order=[('rate', 'ASC')])
            self.assertEqual(len(assets), 2)
            self.assertEqual(assets[0].rate, Decimal('2.6'))
            self.assertEqual(assets[1].rate, Decimal('3.5'))

            assets = Asset.search([], order=[('rate', 'DESC')])
            self.assertEqual(len(assets), 2)
            self.assertEqual(assets[0].rate, Decimal('3.5'))
            self.assertEqual(assets[1].rate, Decimal('2.6'))

            self.assertEqual(Asset.search_count([
                    ('date', '=', date(2022, 5, 17)),
                ]), 1)
            self.assertEqual(Asset.search_count([
                    ('date', '>=', date(2022, 5, 17)),
                ]), 2)
            self.assertEqual(Asset.search_count([
                    ('date', '<', date(2022, 5, 17)),
                ]), 0)

    @with_transaction()
    def test_asset_percentages_dateselect1(self):
        """ create asset, add rates, check selection of
            specific date - fixed date
        """
        Asset = Pool().get('investment.asset')
        cursor = Transaction().connection.cursor()

        company = self.prep_asset_company()
        with Transaction().set_context({'company': company.id}):
            product = self.prep_asset_product(
                name='Product 1',
                description='some asset')

            asset1 = self.prep_asset_item(company=company, product=product)
            self.assertEqual(asset1.rec_name, 'Product 1 | - usd/u | -')

            Asset.write(*[
                [asset1],
                {
                    'rates': [('create', [{
                        'date': date(2022, 5, 15),
                        'rate': Decimal('2.45'),
                        }, {
                        'date': date(2022, 5, 16),
                        'rate': Decimal('2.6'),
                        }, {
                        'date': date(2022, 5, 12),
                        'rate': Decimal('2.0'),
                        }, {
                        'date': date(2022, 5, 3),
                        'rate': Decimal('3.6'),
                        }])],
                },
                ])
            self.assertEqual(
                asset1.rec_name,
                'Product 1 | 2.6000 usd/u | 05/16/2022')
            self.assertEqual(len(asset1.rates), 4)
            self.assertEqual(asset1.rates[0].date, date(2022, 5, 16))
            self.assertEqual(asset1.rates[1].date, date(2022, 5, 15))
            self.assertEqual(asset1.rates[2].date, date(2022, 5, 12))
            self.assertEqual(asset1.rates[3].date, date(2022, 5, 3))

            # query fixed date
            tab_percent = Asset.get_percentage_sql(days=0)
            with Transaction().set_context({
                    'qdate': date(2022, 5, 16)}):
                query = tab_percent.select(
                            tab_percent.id,
                            tab_percent.date,
                            tab_percent.percent,
                            where=tab_percent.id == asset1.id,
                        )
                cursor.execute(*query)
                records = cursor.fetchall()

                # there should be one record, three colums
                self.assertEqual(len(records), 1)
                self.assertEqual(len(records[0]), 3)
                self.assertEqual(records[0][0], asset1.id)
                self.assertEqual(records[0][1], date(2022, 5, 16))
                self.assertEqual(
                    records[0][2].quantize(Decimal('0.01')),
                    Decimal('6.12'))

    @with_transaction()
    def test_asset_percentages_daterange(self):
        """ create asset, add rates, check selection of
            value
        """
        Asset = Pool().get('investment.asset')

        company = self.prep_asset_company()
        with Transaction().set_context({'company': company.id}):
            product = self.prep_asset_product(
                name='Product 1',
                description='some asset')

            asset1 = self.prep_asset_item(company=company, product=product)
            asset2 = self.prep_asset_item(company=company, product=product)

            self.assertEqual(asset1.rec_name, 'Product 1 | - usd/u | -')
            self.assertEqual(asset2.rec_name, 'Product 1 | - usd/u | -')

            Asset.write(*[
                [asset1],
                {
                    'rates': [('create', [{
                        'date': date(2022, 5, 15),
                        'rate': Decimal('2.45'),
                        }, {
                        'date': date(2022, 5, 16),
                        'rate': Decimal('2.6'),
                        }])],
                },
                [asset2],
                {
                    'rates': [('create', [{
                        'date': date(2022, 5, 14),
                        'rate': Decimal('5.75'),
                        }, {
                        'date': date(2022, 5, 15),
                        'rate': Decimal('5.25'),
                        }])],
                },
                ])
            self.assertEqual(
                asset1.rec_name,
                'Product 1 | 2.6000 usd/u | 05/16/2022')
            self.assertEqual(
                asset2.rec_name,
                'Product 1 | 5.2500 usd/u | 05/15/2022')
            self.assertEqual(asset1.change_day1, Decimal('6.12'))
            self.assertEqual(asset2.change_day1, Decimal('-8.7'))
            self.assertEqual(asset1.change_month1, None)
            self.assertEqual(asset2.change_month1, None)
            self.assertEqual(asset1.change_month3, None)
            self.assertEqual(asset2.change_month3, None)
            self.assertEqual(asset1.change_month6, None)
            self.assertEqual(asset2.change_month6, None)
            self.assertEqual(asset1.change_month12, None)
            self.assertEqual(asset2.change_month12, None)

            # check ordering
            assets = Asset.search([
                    ('change_day1', '!=', Decimal('0.0')),
                ], order=[('change_day1', 'ASC')])
            self.assertEqual(len(assets), 2)
            self.assertEqual(assets[0].change_day1, Decimal('-8.7'))
            self.assertEqual(assets[1].change_day1, Decimal('6.12'))

            assets = Asset.search([
                    ('change_day1', '!=', Decimal('0.0')),
                ], order=[('change_day1', 'DESC')])
            self.assertEqual(len(assets), 2)
            self.assertEqual(assets[0].change_day1, Decimal('6.12'))
            self.assertEqual(assets[1].change_day1, Decimal('-8.7'))

            # check 5-day-range
            # four days
            Asset.write(*[
                [asset1],
                {
                    'rates': [('write', [asset1.rates[1]], {
                        'date': date(2022, 5, 12),
                        })],
                }])
            self.assertEqual(asset1.rates[0].date, date(2022, 5, 16))
            self.assertEqual(asset1.rates[1].date, date(2022, 5, 12))
            self.assertEqual(asset1.change_day1, Decimal('6.12'))
            # five days
            Asset.write(*[
                [asset1],
                {
                    'rates': [('write', [asset1.rates[1]], {
                        'date': date(2022, 5, 11),
                        })],
                }])
            self.assertEqual(asset1.rates[0].date, date(2022, 5, 16))
            self.assertEqual(asset1.rates[1].date, date(2022, 5, 11))
            self.assertEqual(asset1.change_day1, Decimal('6.12'))
            # six days
            Asset.write(*[
                [asset1],
                {
                    'rates': [('write', [asset1.rates[1]], {
                        'date': date(2022, 5, 10),
                        })],
                }])
            self.assertEqual(asset1.rates[0].date, date(2022, 5, 16))
            self.assertEqual(asset1.rates[1].date, date(2022, 5, 10))
            self.assertEqual(asset1.change_day1, None)

    @with_transaction()
    def test_asset_percentges_values(self):
        """ create asset, add rates, check percentages
        """
        Asset = Pool().get('investment.asset')

        company = self.prep_asset_company()
        with Transaction().set_context({'company': company.id}):
            product = self.prep_asset_product(
                name='Product 1',
                description='some asset')

            asset1 = self.prep_asset_item(company=company, product=product)

            self.assertEqual(asset1.rec_name, 'Product 1 | - usd/u | -')

            Asset.write(*[
                [asset1],
                {
                    'rates': [('create', [{
                        'date': date(2022, 5, 15),
                        'rate': Decimal('2.45'),
                        }, {
                        'date': date(2022, 5, 16),
                        'rate': Decimal('2.6'),
                        }, {
                        'date': date(2022, 4, 14),
                        'rate': Decimal('2.2'),
                        }, {
                        'date': date(2022, 2, 14),
                        'rate': Decimal('2.8'),
                        },])],
                }])
            self.assertEqual(
                asset1.rec_name,
                'Product 1 | 2.6000 usd/u | 05/16/2022')
            self.assertEqual(len(asset1.rates), 4)
            self.assertEqual(asset1.rates[0].date, date(2022, 5, 16))
            self.assertEqual(asset1.rates[1].date, date(2022, 5, 15))
            self.assertEqual(asset1.rates[2].date, date(2022, 4, 14))
            self.assertEqual(asset1.rates[3].date, date(2022, 2, 14))

            self.assertEqual(asset1.change_day1, Decimal('6.12'))
            self.assertEqual(asset1.change_month1, Decimal('18.18'))
            self.assertEqual(asset1.change_month3, Decimal('-7.14'))
            self.assertEqual(asset1.change_month6, None)
            self.assertEqual(asset1.change_month12, None)

            # call order-functions
            Asset.search([], order=[('change_day1', 'ASC')])
            Asset.search([], order=[('change_month1', 'ASC')])
            Asset.search([], order=[('change_month3', 'ASC')])
            Asset.search([], order=[('change_month6', 'ASC')])
            Asset.search([], order=[('change_month12', 'ASC')])

            # searcher
            self.assertEqual(
                Asset.search_count([('change_day1', '>', Decimal('6.1'))]),
                1)
            self.assertEqual(
                Asset.search_count([('change_day1', '>', Decimal('6.15'))]),
                0)
            self.assertEqual(
                Asset.search_count([('change_day1', '=', Decimal('6.12'))]),
                1)

            self.assertEqual(
                Asset.search_count([('change_month1', '>', Decimal('18.0'))]),
                1)
            self.assertEqual(
                Asset.search_count([('change_month1', '>', Decimal('18.18'))]),
                0)
            self.assertEqual(
                Asset.search_count([('change_month1', '=', Decimal('18.18'))]),
                1)

            self.assertEqual(
                Asset.search_count([('change_month3', '=', Decimal('-7.14'))]),
                1)
            self.assertEqual(
                Asset.search_count([('change_month6', '=', None)]),
                1)

    @with_transaction()
    def test_asset_check_onlinesource_onoff(self):
        """ create asset, switch online-source on/off
        """
        pool = Pool()
        OnlineSource = pool.get('investment.source')

        company = self.prep_asset_company()
        with Transaction().set_context({'company': company.id}):
            product = self.prep_asset_product(
                name='Product 1',
                description='some asset')

            asset = self.prep_asset_item(company=company, product=product)

            o_source, = OnlineSource.create([{
                'name': 'Source 1',
                }])

            self.assertEqual(len(asset.updtsources), 0)
            self.assertEqual(asset.updttime, time(14, 0))

            asset.updtsources = [o_source]
            asset.updttime = time(10, 45)
            asset.save()
            self.assertEqual(len(asset.updtsources), 1)
            self.assertEqual(asset.updtsources[0].rec_name, 'Source 1')
            self.assertEqual(asset.updttime, time(10, 45))

            asset.updtsources = []
            asset.on_change_updtsources()
            self.assertEqual(len(asset.updtsources), 0)
            self.assertEqual(asset.updttime, None)

    @with_transaction()
    def test_asset_check_update_select(self):
        """ create asset, add online-source,
            check selection of assets to update
        """
        pool = Pool()
        OnlineSource = pool.get('investment.source')
        Asset = pool.get('investment.asset')

        company = self.prep_asset_company()
        with Transaction().set_context({'company': company.id}):
            product = self.prep_asset_product(
                name='Product 1',
                description='some asset')

            asset = self.prep_asset_item(company=company, product=product)

            o_source, = OnlineSource.create([{
                'name': 'Source 1',
                }])
            Asset.write(*[
                [asset],
                {
                    'updtsources': [('add', [o_source.id])],
                    'updttime': time(10, 45),
                }])

            with Transaction().set_context({'qdate': date(2022, 10, 14)}):
                # re-read to make context work
                asset2, = Asset.browse([asset.id])

                self.assertEqual(len(asset2.updtsources), 1)
                self.assertEqual(asset2.updtsources[0].rec_name, 'Source 1')
                self.assertEqual(asset2.updttime, time(10, 45))
                self.assertEqual(len(asset2.rates), 0)
                # qdate = 2022-10-14 simulates existence of record at this day
                # next call would be the 15. - but its saturday,
                # next-call-date is moved to 17.
                self.assertEqual(
                    asset2.nextupdate,
                    datetime(2022, 10, 17, 10, 45))

                self.assertEqual(
                    Asset.search_count([
                        ('nextupdate', '<', datetime(2022, 10, 17, 10, 45))]),
                    0)
                self.assertEqual(
                    Asset.search_count([
                        ('nextupdate', '>=', datetime(2022, 10, 17, 10, 45))]),
                    1)

            # add rate at next monday
            Asset.write(*[
                [asset],
                {
                    'rates': [('create', [{
                        'date': date(2022, 10, 17),     # monday
                        'rate': Decimal('1.5'),
                        }])],
                }])
            self.assertEqual(len(asset.rates), 1)

            asset2, = Asset.browse([asset.id])
            self.assertEqual(asset.updtsources[0].rec_name, 'Source 1')
            self.assertEqual(asset.updttime, time(10, 45))
            self.assertEqual(len(asset.rates), 1)
            self.assertEqual(asset.rates[0].date, date(2022, 10, 17))
            self.assertEqual(asset.nextupdate, datetime(2022, 10, 18, 10, 45))

            self.assertEqual(
                Asset.search_count([
                    ('nextupdate', '<', datetime(2022, 10, 18, 10, 45))]),
                0)
            self.assertEqual(
                Asset.search_count([
                    ('nextupdate', '>=', datetime(2022, 10, 18, 10, 45))]),
                1)

            # add rate at today
            Asset.write(*[
                [asset],
                {
                    'rates': [('create', [{
                        'date': date(2022, 10, 18),
                        'rate': Decimal('1.5'),
                        }])],
                }])
            self.assertEqual(len(asset.rates), 2)

            asset2, = Asset.browse([asset.id])
            self.assertEqual(asset2.updtsources[0].rec_name, 'Source 1')
            self.assertEqual(asset2.updttime, time(10, 45))
            self.assertEqual(len(asset2.rates), 2)
            self.assertEqual(asset2.rates[0].date, date(2022, 10, 18))
            self.assertEqual(asset2.nextupdate, datetime(2022, 10, 19, 10, 45))

            self.assertEqual(
                Asset.search_count([
                    ('nextupdate', '<', datetime(2022, 10, 19, 10, 45))]),
                0)
            self.assertEqual(
                Asset.search_count([
                    ('nextupdate', '>=', datetime(2022, 10, 19, 10, 45))]),
                1)

    @with_transaction()
    def test_asset_indentifiers(self):
        """ create asset, add identifiers
        """
        pool = Pool()
        Product = pool.get('product.product')
        Asset = pool.get('investment.asset')

        company = self.prep_asset_company()
        with Transaction().set_context({'company': company.id}):
            product1 = self.prep_asset_product(
                name='Product unit', unit='u')
            product2 = self.prep_asset_product(
                name='Product gram', unit='g')

            asset1 = self.prep_asset_item(company=company, product=product1)
            asset2 = self.prep_asset_item(company=company, product=product2)

            Product.write(*[
                [product1],
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
                },
                [product2],
                {
                    'identifiers': [('create', [{
                        'type': 'wkn',
                        'code': '965310',
                        }, {
                        'type': 'secsymb',
                        'code': '1431157',
                        }, {
                        'type': 'isin',
                        'code': 'XC0009653103',
                        }, ])],
                },
                ])

            self.assertEqual(asset1.wkn, '965515')
            self.assertEqual(asset1.isin, 'XC0009655157')
            self.assertEqual(asset1.secsymb, '1472977')

            self.assertEqual(
                Asset.search_count([('wkn', '=', '965515')]),
                1)
            self.assertEqual(
                Asset.search_count([('isin', '=', 'XC0009655157')]),
                1)
            self.assertEqual(
                Asset.search_count([('secsymb', '=', '1472977')]),
                1)

            self.assertEqual(
                Asset.search_count([('rec_name', '=', '965515')]),
                1)
            self.assertEqual(
                Asset.search_count([('rec_name', '=', 'XC0009655157')]),
                1)
            self.assertEqual(
                Asset.search_count([('rec_name', '=', '1472977')]),
                1)

            self.assertEqual(
                Asset.search_count([('name', '=', '965515')]),
                1)
            self.assertEqual(
                Asset.search_count([('name', '=', 'XC0009655157')]),
                1)
            self.assertEqual(
                Asset.search_count([('name', '=', '1472977')]),
                1)
            self.assertEqual(
                Asset.search_count([('name', '=', 'Product unit')]),
                1)

            self.assertEqual(Asset.search_count([
                    ('wkn', 'ilike', '9655%'),
                ]), 1)
            self.assertEqual(Asset.search_count([
                    ('wkn', 'ilike', '965%'),
                ]), 2)

            self.assertEqual(asset2.wkn, '965310')
            self.assertEqual(asset2.isin, 'XC0009653103')
            self.assertEqual(asset2.secsymb, '1431157')

            # order wkn
            assets = Asset.search([], order=[('wkn', 'ASC')])
            self.assertEqual(len(assets), 2)
            self.assertEqual(assets[0].wkn, '965310')
            self.assertEqual(assets[1].wkn, '965515')
            assets = Asset.search([], order=[('wkn', 'DESC')])
            self.assertEqual(len(assets), 2)
            self.assertEqual(assets[0].wkn, '965515')
            self.assertEqual(assets[1].wkn, '965310')

            # order isin
            assets = Asset.search([], order=[('isin', 'ASC')])
            self.assertEqual(len(assets), 2)
            self.assertEqual(assets[0].isin, 'XC0009653103')
            self.assertEqual(assets[1].isin, 'XC0009655157')
            assets = Asset.search([], order=[('wkn', 'DESC')])
            self.assertEqual(len(assets), 2)
            self.assertEqual(assets[0].isin, 'XC0009655157')
            self.assertEqual(assets[1].isin, 'XC0009653103')

            # order secsymb
            assets = Asset.search([], order=[('secsymb', 'ASC')])
            self.assertEqual(len(assets), 2)
            self.assertEqual(assets[0].secsymb, '1431157')
            self.assertEqual(assets[1].secsymb, '1472977')
            assets = Asset.search([], order=[('wkn', 'DESC')])
            self.assertEqual(len(assets), 2)
            self.assertEqual(assets[0].secsymb, '1472977')
            self.assertEqual(assets[1].secsymb, '1431157')

    @with_transaction()
    def test_asset_check_product_update(self):
        """ check update of product on asset
        """
        company = self.prep_asset_company()
        with Transaction().set_context({'company': company.id}):
            product1 = self.prep_asset_product(
                name='Product unit', unit='u')
            product2 = self.prep_asset_product(
                name='Product gram', unit='g')
            self.assertEqual(product2.default_uom.digits, 2)

            asset = self.prep_asset_item(company=company, product=product1)

            self.assertEqual(asset.product.rec_name, 'Product unit')
            self.assertEqual(asset.product.default_uom.rec_name, 'Unit')
            self.assertEqual(asset.uom.rec_name, 'Unit')
            self.assertEqual(asset.currency_digits, 4)

            asset.product = product2
            asset.on_change_product()
            asset.save()

            self.assertEqual(asset.product.rec_name, 'Product gram')
            self.assertEqual(asset.product.default_uom.rec_name, 'Gram')
            self.assertEqual(asset.uom.rec_name, 'Gram')

            asset.on_change_currency()
            asset.save()
            self.assertEqual(asset.currency_digits, 2)

# end AssetTestCase
