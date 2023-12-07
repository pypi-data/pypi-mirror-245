# -*- coding: utf-8 -*-
# This file is part of the investment-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from sql.functions import Function
from datetime import timedelta


class Concat2(Function):
    """ concat columns
    """
    __slots__ = ()
    _function = 'concat'

# end Concat2


class GraphDef(metaclass=PoolMeta):
    __name__ = 'diagram.graphdef'

    asset = fields.Many2One(
        string='Asset', model_name='investment.asset',
        states={
            'invisible': Eval('dtype', '') != 'investment.asset',
            'required': Eval('dtype', '') == 'investment.asset',
        }, depends=['dtype'])

    @classmethod
    def _get_dtypes(cls):
        """ return list of types
        """
        l1 = super(GraphDef, cls)._get_dtypes()
        l1.append('investment.asset')
        return l1

    def get_recname_value(self):
        """ value by dtype
        """
        if self.dtype == 'investment.asset':
            return getattr(self.asset, 'rec_name', '-')
        return super(GraphDef, self).get_recname_value()

    def get_field_key(self):
        """ get to read value from json
        """
        if self.dtype == 'investment.asset':
            return 'asset%d' % self.asset.id
        return super(GraphDef, self).get_field_key()

    def get_scaling_for_investment_asset(self):
        """ get scaling for currency
        """
        Rate = Pool().get('investment.rate')

        if self.scaling == 'fix':
            return None

        if self.scaling == 'alldata':
            query = [('asset', '=', self.asset.id)]
        elif self.scaling == 'view':
            query = [
                ('asset', '=', self.asset.id),
                ('date', '>=', self.chart.used_start_date()),
                ('date', '<=', self.chart.used_end_date()),
                ]
        elif self.scaling == 'six':
            query = [
                ('asset', '=', self.asset.id),
                ('date', '>=', self.chart.used_start_date() -
                    timedelta(days=180)),
                ('date', '<=', self.chart.used_end_date()),
                ]

        min_rec = Rate.search(query, limit=1, order=[('rate', 'ASC')])
        max_rec = Rate.search(query, limit=1, order=[('rate', 'DESC')])
        min_val = min_rec[0].rate if len(min_rec) > 0 else None
        max_val = max_rec[0].rate if len(max_rec) > 0 else None

        return self.compute_scaling_factor(min_val, max_val)

# end GraphDef


class ChartPoint(metaclass=PoolMeta):
    __name__ = 'diagram.point'

    @classmethod
    def get_interpolated_val(cls, keyname, query_date):
        """ query two neighbour-values to
            interpolate missing value
        """
        Rate = Pool().get('investment.rate')

        if keyname is None:
            return None

        # check if query is for us
        if keyname.startswith('asset'):
            asset_id = int(keyname[len('asset'):])

            before = Rate.search([
                ('date', '<', query_date),
                ('asset', '=', asset_id),
                ], limit=1, order=[('date', 'DESC')])

            after = Rate.search([
                ('date', '>', query_date),
                ('asset', '=', asset_id),
                ], limit=1, order=[('date', 'ASC')])

            if (len(before) == 1) and (len(after) == 1):
                result = cls.interpolate_linear(
                        (after[0].date, after[0].rate),
                        (before[0].date, before[0].rate),
                        query_date
                    )
                return result
            elif len(before) == 1:
                return before[0].rate
            elif len(after) == 1:
                return after[0].rate
        return super(ChartPoint, cls).get_interpolated_val(keyname, query_date)

    @classmethod
    def get_table_parts(cls):
        """ return a list of tables to union,
            table must contain the columns:
                date, key, val
        """
        pool = Pool()
        Rate = pool.get('investment.rate')
        tab_rate = Rate.__table__()

        tabparts = super(ChartPoint, cls).get_table_parts()

        # rate
        tabparts.append(tab_rate.select(
                tab_rate.date,
                Concat2('asset', tab_rate.asset).as_('key'),
                tab_rate.rate.as_('val'),
            ))
        return tabparts

# end ChartPoint
