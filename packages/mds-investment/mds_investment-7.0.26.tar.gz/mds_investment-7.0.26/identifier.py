# -*- coding: utf-8 -*-
# This file is part of the investment-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.pool import PoolMeta


class Identifier(metaclass=PoolMeta):
    __name__ = 'product.identifier'

    @classmethod
    def __setup__(cls):
        super(Identifier, cls).__setup__()
        cls.type.selection.extend([
            ('wkn', 'National Securities Identifying Number (NSIN)'),
            ('secsymb', 'Stock market symbol'),
            ])

# end Identifier
