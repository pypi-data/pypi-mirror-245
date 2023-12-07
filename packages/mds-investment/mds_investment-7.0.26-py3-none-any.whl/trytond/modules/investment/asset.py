# -*- coding: utf-8 -*-
# This file is part of the investment-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields, SymbolMixin, Index
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.pyson import Eval, Bool, If, Date
from trytond.report import Report

from decimal import Decimal
from datetime import time
from sql.functions import CurrentDate, CurrentTimestamp, Round, Extract
from sql.conditionals import Case, Coalesce, NullIf
from sql import Literal
from .diagram import Concat2
from .const import DEF_NONE


digits_percent = 2

sel_updtdays = [
        ('work', 'Mon - Fri'),
        ('week', 'Mon - Sun'),
    ]


class Asset(SymbolMixin, ModelSQL, ModelView):
    'Asset'
    __name__ = 'investment.asset'

    name = fields.Function(fields.Char(
        string='Name', readonly=True),
            'get_name_symbol', searcher='search_rec_name')
    company = fields.Many2One(
        string='Company', model_name='company.company',
        required=True, ondelete="RESTRICT")
    product = fields.Many2One(
        string='Product', required=True, model_name='product.product',
        ondelete='RESTRICT', domain=[('type', '=', 'assets')])
    product_uom = fields.Function(fields.Many2One(
        string='UOM Category', readonly=True,
        model_name='product.uom.category',
        help='Category of unit on the product.'), 'get_name_symbol')
    uom = fields.Many2One(
        string='UOM', required=True, model_name='product.uom',
        ondelete='RESTRICT',
        states={
            'readonly': ~Bool(Eval('product')),
        },
        domain=[
            ('category', '=', Eval('product_uom')),
        ], depends=['product_uom', 'product'])
    symbol = fields.Function(fields.Char(
        string='UOM', readonly=True), 'get_name_symbol',
        searcher='search_uom_symbol')
    asset_symbol = fields.Function(fields.Many2One(
        string='Symbol', readonly=True, model_name='investment.asset'),
        'get_name_symbol')

    rates = fields.One2Many(
        string='Rates', field='asset', model_name='investment.rate')
    rate = fields.Function(fields.Numeric(
        string='Current Rate', readonly=True,
        digits=(16, Eval('currency_digits', 4)), depends=['currency_digits']),
        'get_rate_data', searcher='search_rate')
    date = fields.Function(fields.Date(
        string='Date', readonly=True, help='Date of current rate'),
        'get_rate_data', searcher='search_date')

    currency = fields.Many2One(
        string='Currency', required=True,
        model_name='currency.currency', ondelete='RESTRICT')
    currency_digits = fields.Integer(
        string='Digits', required=True,
        domain=[
            ('currency_digits', '>=', 0),
            ('currency_digits', '<=', 6)])

    wkn = fields.Function(fields.Char(
        string='NSIN', readonly=True,
        help='National Securities Identifying Number'),
        'get_identifiers', searcher='search_identifier')
    isin = fields.Function(fields.Char(
        string='ISIN', readonly=True,
        help='International Securities Identification Number'),
        'get_identifiers', searcher='search_identifier')
    secsymb = fields.Function(fields.Char(
        string='Symbol', readonly=True,
        help='Stock market symbol'),
        'get_identifiers', searcher='search_identifier')

    updtsources = fields.Many2Many(
        string='Update Sources',
        help='Select sources for the course update. The course sources ' +
        'are tried until a valid value has been read.',
        relation_name='investment.asset_source_rel',
        origin='asset', target='source')
    updturl = fields.Char(
        string='URL',
        help='URL for data retrieval.',
        states={
            'invisible': ~Eval('updturl_enable', False),
            'required': Eval('updturl_enable', False),
        }, depends=['updturl_enable'])
    updturl_enable = fields.Function(fields.Boolean(
        string='URL required', readonly=True,
        states={'invisible': True}),
        'on_change_with_updturl_enable')
    updtdays = fields.Selection(
        string='Select days', required=True, selection=sel_updtdays)
    updttime = fields.Time(
        string='Time',
        states={
            'readonly': ~Bool(Eval('updtsources')),
        }, depends=['updtsources'])
    nextupdate = fields.Function(fields.DateTime(
        string='Next Update', readonly=True),
        'get_nextupdates', searcher='search_nextupdate')

    # percentage change
    change_day1 = fields.Function(fields.Numeric(
        string='Previous Day', readonly=True,
        digits=(16, digits_percent)),
        'get_percentage_change', searcher='search_percentage')
    change_month1 = fields.Function(fields.Numeric(
        string='1 Month', readonly=True,
        help='percentage change in value compared to last month',
        digits=(16, digits_percent)),
        'get_percentage_change', searcher='search_percentage')
    change_month3 = fields.Function(fields.Numeric(
        string='3 Months',
        help='percentage change in value during 3 months',
        digits=(16, digits_percent)),
        'get_percentage_change', searcher='search_percentage')
    change_month6 = fields.Function(fields.Numeric(
        string='6 Months', readonly=True,
        help='percentage change in value during 6 months',
        digits=(16, digits_percent)),
        'get_percentage_change', searcher='search_percentage')
    change_month12 = fields.Function(fields.Numeric(
        string='1 Year', readonly=True,
        help='percentage change in value during 1 year',
        digits=(16, digits_percent)),
        'get_percentage_change', searcher='search_percentage')
    change_symbol = fields.Function(fields.Many2One(
        string='Symbol', readonly=True, model_name='investment.rate'),
        'get_rate_data')

    @classmethod
    def __register__(cls, module_name):
        """ register and migrate
        """
        super(Asset, cls).__register__(module_name)
        cls.migrate_updtsource(module_name)

    @classmethod
    def __setup__(cls):
        super(Asset, cls).__setup__()
        cls._order.insert(0, ('name', 'ASC'))
        cls._order.insert(0, ('date', 'DESC'))
        t = cls.__table__()
        cls._sql_indexes.update({
            Index(
                t,
                (t.product, Index.Equality())),
            Index(
                t,
                (t.currency, Index.Equality())),
            Index(
                t,
                (t.uom, Index.Equality())),
            Index(
                t,
                (t.updtdays, Index.Equality())),
            })

    @classmethod
    def migrate_updtsource(cls, module_name):
        """ replace 'updtsource' by relation
        """
        pool = Pool()
        Asset2 = pool.get('investment.asset')

        asset_table = Asset2.__table_handler__(module_name)
        if asset_table.column_exist('updtsource'):
            AssetSourceRel = pool.get('investment.asset_source_rel')
            tab_asset = Asset2.__table__()
            cursor = Transaction().connection.cursor()

            query = tab_asset.select(
                    tab_asset.id,
                    tab_asset.updtsource,
                    where=tab_asset.updtsource != DEF_NONE,
                )
            cursor.execute(*query)
            records = cursor.fetchall()
            to_create = [{
                    'asset': x[0],
                    'source': x[1],
                } for x in records]

            if len(to_create) > 0:
                AssetSourceRel.create(to_create)
            asset_table.drop_column('updtsource')

    @classmethod
    def view_attributes(cls):
        return super().view_attributes() + [
            ('/tree', 'visual',
                If(Eval('date', Date()) < Date(delta_days=-5), 'muted',
                    If(Eval('change_day1', 0) < 0, 'danger',
                        If(Eval('change_day1', 0) > 0, 'success', '')))),
            ]

    @classmethod
    def default_currency(cls):
        """ currency of company
        """
        Company = Pool().get('company.company')

        company = cls.default_company()
        if company:
            company = Company(company)
            if company.currency:
                return company.currency.id

    @staticmethod
    def default_company():
        return Transaction().context.get('company') or None

    @classmethod
    def default_currency_digits(cls):
        """ default: 4
        """
        return 4

    @classmethod
    def default_updttime(cls):
        """ 14 o'clock UTC
        """
        return time(14, 0)

    @classmethod
    def default_updtdays(cls):
        """ default: mon - fri
        """
        return 'work'

    @fields.depends('updtsources')
    def on_change_with_updturl_enable(self, name=None):
        """ return True if a source has fixed-url
        """
        if self.updtsources:
            for usource in self.updtsources:
                if usource.fixed_url is True:
                    return True
        return False

    @fields.depends('updtsources', 'updttime')
    def on_change_updtsources(self):
        """ clear time-fields
        """
        if len(self.updtsources) == 0:
            self.updttime = None
        else:
            self.updttime = time(11, 30)

    @fields.depends('product', 'uom')
    def on_change_product(self):
        """ update unit by product
        """
        if self.product:
            self.uom = self.product.default_uom
            return
        self.uom = None

    @fields.depends('currency', 'currency_digits')
    def on_change_currency(self):
        """ update currency_digits by value on currency
        """
        if self.currency:
            self.currency_digits = self.currency.digits

    @classmethod
    def get_name_symbol_sql(cls):
        """ get sql for name, uom, digits, etc.
        """
        pool = Pool()
        Product = pool.get('product.product')
        ProdTempl = pool.get('product.template')
        Uom = pool.get('product.uom')
        Currency = pool.get('currency.currency')
        tab_asset = cls.__table__()
        tab_templ = ProdTempl.__table__()
        tab_prod = Product.__table__()
        tab_uom = Uom.__table__()
        tab_cur = Currency.__table__()

        # get translated symbol-column from UOM
        (tab1, join1, col1) = Uom.symbol._get_translation_column(Uom, 'symbol')
        tab_symb = join1.select(tab1.id, col1.as_('symbol'))

        query = tab_asset.join(
                tab_prod,
                condition=tab_asset.product == tab_prod.id,
            ).join(
                tab_templ,
                condition=tab_templ.id == tab_prod.template,
            ).join(
                tab_uom,
                condition=tab_templ.default_uom == tab_uom.id,
            ).join(
                tab_cur,
                condition=tab_asset.currency == tab_cur.id,
            ).join(
                tab_symb,
                condition=tab_asset.uom == tab_symb.id,
            ).select(
                tab_asset.id,
                tab_templ.name,
                tab_uom.category.as_('product_uom'),
                Concat2(tab_cur.symbol, '/', tab_symb.symbol).as_('symbol'),
            )
        return (query, tab_asset)

    @classmethod
    def get_name_symbol(cls, assets, names):
        """ get date and rate of asset
        """
        cursor = Transaction().connection.cursor()

        result = {x: {y.id: None for y in assets} for x in names}

        (query, tab_asset) = cls.get_name_symbol_sql()
        if assets:
            query.where = tab_asset.id.in_([x.id for x in assets])
            cursor.execute(*query)
            records = cursor.fetchall()

            for record in records:
                values = {
                    'name': record[1],
                    'product_uom': record[2],
                    'symbol': record[3],
                    'asset_symbol': record[0],
                    }

                for name in names:
                    result[name][record[0]] = values[name]
        return result

    @classmethod
    def search_uom_symbol(cls, names, clause):
        """ search in uom
        """
        return ['OR',
                (('uom.rec_name',) + tuple(clause[1:])),
                (('currency.rec_name',) + tuple(clause[1:]))]

    @classmethod
    def get_rate_data_sql(cls):
        """ get sql for rate/date
        """
        pool = Pool()
        Asset = pool.get('investment.asset')
        Rate = pool.get('investment.rate')
        tab_asset = Asset.__table__()
        tab_rate = Rate.__table__()

        query = tab_asset.join(
                tab_rate,
                condition=tab_asset.id == tab_rate.asset
            ).select(
                tab_asset.id,
                Round(tab_rate.rate, tab_asset.currency_digits).as_('rate'),
                tab_rate.date,
                tab_rate.id.as_('id_rate'),
                distinct_on=[tab_asset.id],
                order_by=[tab_asset.id, tab_rate.date.desc],
            )
        return (query, tab_asset)

    @classmethod
    def get_rate_data(cls, assets, names):
        """ get date and rate of asset
        """
        cursor = Transaction().connection.cursor()

        result = {x: {y.id: None for y in assets} for x in names}

        if assets:
            (query, tab_asset) = cls.get_rate_data_sql()
            query.where = tab_asset.id.in_([x.id for x in assets])
            curr_digits = {x.id: x.currency_digits for x in assets}

            cursor.execute(*query)
            records = cursor.fetchall()

            for record in records:
                (id1, rate1, date1, id_rate) = record

                curr_dig = curr_digits.get(id1, 4)
                exp = Decimal(Decimal(1) / 10 ** curr_dig)

                values = {
                    'rate': record[1].quantize(exp),
                    'date': record[2],
                    'change_symbol': id_rate,
                    }

                for name in names:
                    result[name][record[0]] = values[name]
        return result

    @classmethod
    def search_date(cls, names, clause):
        """ search in date
        """
        (tab_query, tab_asset) = cls.get_rate_data_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]

        query = tab_query.select(
                tab_query.id,
                where=Operator(tab_query.date, clause[2]),
            )
        return [('id', 'in', query)]

    @classmethod
    def search_rate(cls, names, clause):
        """ search in rate
        """
        (tab_query, tab_asset) = cls.get_rate_data_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]

        query = tab_query.select(
                tab_query.id,
                where=Operator(tab_query.rate, clause[2]),
            )
        return [('id', 'in', query)]

    @staticmethod
    def order_date(tables):
        """ order date
        """
        (tab_query, tab_asset) = Asset.get_rate_data_sql()
        table, _ = tables[None]

        query = tab_query.select(
                tab_query.date,
                where=tab_query.id == table.id,
            )
        return [query]

    @staticmethod
    def order_rate(tables):
        """ order rate
        """
        (tab_query, tab_asset) = Asset.get_rate_data_sql()
        table, _ = tables[None]

        query = tab_query.select(
                tab_query.rate,
                where=tab_query.id == table.id,
            )
        return [query]

    @classmethod
    def get_percentage_sql(cls, days=0, asset_ids=None):
        """ get table for percentages and dates,
            days: delta-days to past to select percent-value
                0=yesterday, 30=last month, ...
        """
        pool = Pool()
        Rate = pool.get('investment.rate')
        tab_rate1 = Rate.__table__()
        tab_rate2 = Rate.__table__()
        context = Transaction().context

        query_date = context.get('qdate', CurrentDate())
        where_asset = tab_rate1.date <= query_date
        if isinstance(asset_ids, list):
            where_asset &= tab_rate1.asset.in_(asset_ids)

        tab_today = tab_rate1.select(
                tab_rate1.asset.as_('id'),
                tab_rate1.date,
                tab_rate1.rate,
                distinct_on=[tab_rate1.asset],
                order_by=[tab_rate1.asset, tab_rate1.date.desc],
                where=where_asset,
            )

        days_diff = days + 5
        query = tab_today.join(
                tab_rate2,
                condition=(tab_today.id == tab_rate2.asset) &
                (tab_today.date > (tab_rate2.date + days)) &
                (tab_today.date <= (tab_rate2.date + days_diff)),
                type_='LEFT OUTER',
            ).select(
                tab_today.id,
                tab_today.date,
                tab_today.rate,
                (tab_today.rate * 100.0 / NullIf(tab_rate2.rate, 0.00) -
                    100.0).as_('percent'),
                distinct_on=[tab_today.id],
                order_by=[tab_today.id, tab_rate2.date.desc]
            )
        return query

    @staticmethod
    def order_change_day1(tables):
        """ order day1
        """
        Asset2 = Pool().get('investment.asset')
        tab_asset = Asset2.get_percentage_sql(days=0)
        table, _ = tables[None]

        query = tab_asset.select(
                tab_asset.percent,
                where=tab_asset.id == table.id,
            )
        return [query]

    @staticmethod
    def order_change_month1(tables):
        """ order month1
        """
        Asset2 = Pool().get('investment.asset')
        tab_asset = Asset2.get_percentage_sql(days=30)
        table, _ = tables[None]

        query = tab_asset.select(
                tab_asset.percent,
                where=tab_asset.id == table.id,
            )
        return [query]

    @staticmethod
    def order_change_month3(tables):
        """ order month1
        """
        Asset2 = Pool().get('investment.asset')
        tab_asset = Asset2.get_percentage_sql(days=90)
        table, _ = tables[None]

        query = tab_asset.select(
                tab_asset.percent,
                where=tab_asset.id == table.id,
            )
        return [query]

    @staticmethod
    def order_change_month6(tables):
        """ order month1
        """
        Asset2 = Pool().get('investment.asset')
        tab_asset = Asset2.get_percentage_sql(days=180)
        table, _ = tables[None]

        query = tab_asset.select(
                tab_asset.percent,
                where=tab_asset.id == table.id,
            )
        return [query]

    @staticmethod
    def order_change_month12(tables):
        """ order month1
        """
        Asset2 = Pool().get('investment.asset')
        tab_asset = Asset2.get_percentage_sql(days=365)
        table, _ = tables[None]

        query = tab_asset.select(
                tab_asset.percent,
                where=tab_asset.id == table.id,
            )
        return [query]

    @classmethod
    def search_percentage(cls, names, clause):
        """ search for percentages
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        field_name = clause[0][len('change_'):]
        tab_percent = cls.get_percentage_sql(days={
            'day1': 0,
            'month1': 30,
            'month3': 90,
            'month6': 180,
            'month12': 365,
            }[field_name])

        query = tab_percent.select(
            tab_percent.id,
            where=Operator(Round(tab_percent.percent, 2), clause[2]))
        return [('id', 'in', query)]

    @classmethod
    def get_percentage_change(cls, assets, names):
        """ get percentage per period
        """
        cursor = Transaction().connection.cursor()

        result = {x: {y.id: None for y in assets} for x in names}
        exp = Decimal(Decimal(1) / 10 ** digits_percent)
        asset_id_lst = [x.id for x in assets]

        if asset_id_lst and names:
            for x in names:
                tab_percent = cls.get_percentage_sql(
                    days={
                        'change_day1': 0,
                        'change_month1': 30,
                        'change_month3': 90,
                        'change_month6': 180,
                        'change_month12': 365,
                        }[x],
                    asset_ids=asset_id_lst,
                    )
                cursor.execute(*tab_percent)
                records = cursor.fetchall()

                for record in records:
                    result[x][record[0]] = record[3].quantize(exp) \
                            if record[3] is not None else None
        return result

    @classmethod
    def get_next_update_datetime_sql(cls):
        """ get sql for datetime of next planned update
        """
        pool = Pool()
        Asset = pool.get('investment.asset')
        AssetSourceRel = pool.get('investment.asset_source_rel')
        Rate = pool.get('investment.rate')
        tab_asset = Asset.__table__()
        tab_rate = Rate.__table__()
        tab_rel = AssetSourceRel.__table__()
        context = Transaction().context

        query_date = context.get('qdate', CurrentDate() - Literal(1))

        # get last date of rate
        tab_date = tab_asset.join(
                tab_rel,
                # link to asset-source-relation to check if
                # there are online-sources set
                condition=tab_rel.asset == tab_asset.id,
            ).join(
                tab_rate,
                condition=tab_asset.id == tab_rate.asset,
                type_='LEFT OUTER',
            ).select(
                tab_asset.id,
                (Coalesce(tab_rate.date, query_date) + Literal(1)).as_('date'),
                tab_asset.updtdays,
                tab_asset.updttime,
                distinct_on=[tab_asset.id],
                order_by=[tab_asset.id, tab_rate.date.desc],
            )

        query = tab_date.select(
            tab_date.id,
            (Case(
                ((tab_date.updtdays == 'work') &
                    (Extract('dow', tab_date.date) == 0),
                    tab_date.date + Literal(1)),
                ((tab_date.updtdays == 'work') &
                    (Extract('dow', tab_date.date) == 6),
                    tab_date.date + Literal(2)),
                else_=tab_date.date,
                ) + tab_date.updttime).as_('updttime'),
            )
        return query

    @classmethod
    def get_nextupdates(cls, assets, names):
        """ get timestamp of next update
        """
        Asset2 = Pool().get('investment.asset')
        tab_updt = Asset2.get_next_update_datetime_sql()
        cursor = Transaction().connection.cursor()

        query = tab_updt.select(
                tab_updt.id,
                tab_updt.updttime,
                where=tab_updt.id.in_([x.id for x in assets]),
            )
        cursor.execute(*query)
        records = cursor.fetchall()

        result = {x: {y.id: None for y in assets} for x in names}

        for record in records:
            (id1, updt) = record
            r1 = {'nextupdate': updt}

            for n in names:
                result[n][id1] = r1[n]
        return result

    @classmethod
    def search_nextupdate(cls, names, clause):
        """ search for assets to update
        """
        Asset2 = Pool().get('investment.asset')
        tab_updt = Asset2.get_next_update_datetime_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]

        query = tab_updt.select(
                tab_updt.id,
                where=Operator(tab_updt.updttime, clause[2]),
            )
        return [('id', 'in', query)]

    @classmethod
    def get_identifier_sql(cls, tab_asset):
        """ sql-query for identifiers
        """
        pool = Pool()
        Product = pool.get('product.product')
        Identifier = pool.get('product.identifier')
        tab_prod = Product.__table__()
        tab_wkn = Identifier.__table__()
        tab_secsymb = Identifier.__table__()
        tab_isin = Identifier.__table__()

        query = tab_asset.join(
                tab_prod,
                condition=tab_asset.product == tab_prod.id,
            ).join(
                tab_wkn,
                condition=(tab_prod.id == tab_wkn.product) &
                (tab_wkn.type == 'wkn'),
                type_='LEFT OUTER',
            ).join(
                tab_secsymb,
                condition=(tab_prod.id == tab_secsymb.product) &
                (tab_secsymb.type == 'secsymb'),
                type_='LEFT OUTER',
            ).join(
                tab_isin,
                condition=(tab_prod.id == tab_isin.product) &
                (tab_isin.type == 'isin'),
                type_='LEFT OUTER',
            ).select(
                tab_asset.id,
                tab_wkn.code.as_('wkn'),
                tab_secsymb.code.as_('secsymb'),
                tab_isin.code.as_('isin'),
            )
        return query

    @staticmethod
    def order_name(tables):
        """ order name
        """
        pool = Pool()
        Templ = pool.get('product.template')
        Product = pool.get('product.product')
        Asset = pool.get('investment.asset')
        table, _ = tables[None]
        tab_asset = Asset.__table__()
        tab_prod = Product.__table__()
        tab_templ = Templ.__table__()

        query = tab_asset.join(
                tab_prod,
                condition=tab_asset.product == tab_prod.id
            ).join(
                tab_templ,
                condition=tab_templ.id == tab_prod.template
            ).select(
                tab_templ.name,
                where=tab_asset.id == table.id
            )
        return [query]

    @staticmethod
    def order_wkn(tables):
        """ order wkn
        """
        Asset = Pool().get('investment.asset')
        tab_ids = Asset.get_identifier_sql(Asset.__table__())
        table, _ = tables[None]

        query = tab_ids.select(
                getattr(tab_ids, 'wkn'),
                where=tab_ids.id == table.id,
            )
        return [query]

    @staticmethod
    def order_isin(tables):
        """ order isin
        """
        Asset = Pool().get('investment.asset')
        tab_ids = Asset.get_identifier_sql(Asset.__table__())
        table, _ = tables[None]

        query = tab_ids.select(
                getattr(tab_ids, 'isin'),
                where=tab_ids.id == table.id,
            )
        return [query]

    @staticmethod
    def order_secsymb(tables):
        """ order secsymb
        """
        Asset = Pool().get('investment.asset')
        tab_ids = Asset.get_identifier_sql(Asset.__table__())
        table, _ = tables[None]

        query = tab_ids.select(
                getattr(tab_ids, 'secsymb'),
                where=tab_ids.id == table.id,
            )
        return [query]

    @classmethod
    def search_identifier(cls, names, clause):
        """ search in identifier
        """
        pool = Pool()
        Asset = pool.get('investment.asset')
        tab_asset = Asset.__table__()
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_ids = cls.get_identifier_sql(tab_asset)

        field_qu = getattr(tab_ids, names)
        query = tab_ids.join(
                tab_asset,
                condition=tab_ids.id == tab_asset.id,
            ).select(
                tab_asset.id,
                where=Operator(field_qu, clause[2]) &
                (field_qu != DEF_NONE),
            )

        return [('id', 'in', query)]

    @classmethod
    def get_identifiers(cls, assets, names):
        """ get identifiers of assets
        """
        pool = Pool()
        Asset = pool.get('investment.asset')
        tab_asset = Asset.__table__()
        cursor = Transaction().connection.cursor()

        result = {x: {y.id: None for y in assets} for x in names}
        if assets:
            query = cls.get_identifier_sql(tab_asset)
            query.where = tab_asset.id.in_([x.id for x in assets])

            cursor.execute(*query)
            l1 = cursor.fetchall()

            for x in l1:
                (id1, wkn, secsymb, isin) = x
                r1 = {'wkn': wkn, 'secsymb': secsymb, 'isin': isin}

                for n in names:
                    result[n][id1] = r1[n]
        return result

    def get_rec_name(self, name):
        """ record name
        """
        return '%(prod)s | %(rate)s %(unit)s | %(date)s' % {
            'prod': getattr(self.product, 'rec_name', '-'),
            'unit': self.symbol,
            'rate': Report.format_number(
                self.rate, lang=None, digits=self.currency_digits or 4)
            if self.rate is not None else '-',
            'date': Report.format_date(self.date)
            if self.date is not None else '-'}

    @classmethod
    def search_rec_name(cls, name, clause):
        """ search in rec_name
        """
        return [
            'OR',
            ('product.rec_name',) + tuple(clause[1:]),
            ('product.identifiers.code',) + tuple(clause[1:]),
            ]

    @classmethod
    def after_update_actions(cls, assets):
        """ run activities after rate-update
        """
        pass

    @classmethod
    def cron_update(cls):
        """ update asset-rates
        """
        pool = Pool()
        Asset2 = pool.get('investment.asset')
        OnlineSource = pool.get('investment.source')
        context = Transaction().context

        query_time = context.get('qdatetime', CurrentTimestamp())
        to_run_activities = []
        for asset in Asset2.search([
                ('nextupdate', '<=', query_time)]):
            if OnlineSource.update_rate(asset):
                to_run_activities.append(asset)

        if len(to_run_activities) > 0:
            cls.after_update_actions(to_run_activities)

# end Asset


class AssetSourceRel(ModelSQL):
    'Asset Source Relation'
    __name__ = 'investment.asset_source_rel'

    source = fields.Many2One(
        string='Online Source',
        required=True, model_name='investment.source',
        ondelete='CASCADE')
    asset = fields.Many2One(
        string='Asset',
        required=True, model_name='investment.asset',
        ondelete='CASCADE')

# end AssetSourceRel
