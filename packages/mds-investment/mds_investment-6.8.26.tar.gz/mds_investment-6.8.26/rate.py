# -*- coding: utf-8 -*-
# This file is part of the investment-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.model import (
        ModelView, ModelSQL, fields, Unique, Check, SymbolMixin, Index)
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.pyson import Eval


class Rate(SymbolMixin, ModelSQL, ModelView):
    'Rate'
    __name__ = 'investment.rate'

    asset = fields.Many2One(
        string='Asset', required=True, ondelete='CASCADE',
        model_name='investment.asset')
    date = fields.Date(string='Date', required=True)
    rate = fields.Numeric(
        string='Rate', required=True,
        digits=(16, Eval('asset_digits', 4)), depends=['asset_digits'])

    asset_digits = fields.Function(fields.Integer(
        string='Digits', readonly=True), 'get_rate_data')
    currency = fields.Function(fields.Many2One(
        string='Currency', readonly=True, model_name='currency.currency'),
        'get_rate_data')
    uom = fields.Function(fields.Many2One(
        string='Uom', readonly=True, model_name='product.uom'),
        'get_rate_data')
    symbol = fields.Function(fields.Char(
        string='Symbol', readonly=True), 'get_rate_data')

    @classmethod
    def __setup__(cls):
        super(Rate, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints = [
            ('date_asset_uniq',
                Unique(t, t.date, t.asset),
                'investment.msg_unique_rate_date'),
            ('check_rate',
                Check(t, t.rate >= 0),
                'currency.msg_rate_positive'),
            ]
        cls._order.insert(0, ('date', 'DESC'))
        cls._sql_indexes.update({
            Index(
                t,
                (t.date, Index.Range(order='DESC'))),
            Index(
                t,
                (t.rate, Index.Range())),
            Index(
                t,
                (t.asset, Index.Equality())),
            Index(
                t,
                (t.asset, Index.Equality()),
                (t.date, Index.Range(order='DESC'))),
            })

    @classmethod
    def default_date(cls):
        """ today
        """
        IrDate = Pool().get('ir.date')
        return IrDate.today()

    @classmethod
    def get_rate_data(cls, rates, names):
        """ speed up: get values for rate
        """
        pool = Pool()
        Asset = pool.get('investment.asset')
        tab_asset = Asset.__table__()
        tab_rate = cls.__table__()
        cursor = Transaction().connection.cursor()

        query = tab_asset.join(
                tab_rate,
                condition=tab_asset.id == tab_rate.asset,
            ).select(
                tab_rate.id,
                tab_asset.uom,
                tab_asset.currency,
                tab_asset.currency_digits,
                where=tab_rate.id.in_([x.id for x in rates]),
            )
        cursor.execute(*query)
        records = cursor.fetchall()

        result = {x: {y.id: None for y in rates} for x in names}
        for record in records:
            r1 = {
                'symbol': '%',
                'uom': record[1],
                'currency': record[2],
                'asset_digits': record[3],
                }

            for n in names:
                result[n][record[0]] = r1[n]
        return result

# Rate
