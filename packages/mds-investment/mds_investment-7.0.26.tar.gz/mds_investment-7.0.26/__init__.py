# -*- coding: utf-8 -*-
# This file is part of the investment-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.pool import Pool
from .asset import Asset, AssetSourceRel
from .rate import Rate
from .identifier import Identifier
from .cron import Cron
from .onlinesource import OnlineSource
from .update_wiz import UpdateSoureWizard
from .diagram import GraphDef, ChartPoint
from .import_wiz import ImportWizard, ImportWizardStart


def register():
    Pool.register(
        OnlineSource,
        AssetSourceRel,
        Asset,
        Rate,
        Identifier,
        Cron,
        ImportWizardStart,
        module='investment', type_='model')
    Pool.register(
        GraphDef,
        ChartPoint,
        module='investment', type_='model', depends=['diagram'])
    Pool.register(
        UpdateSoureWizard,
        ImportWizard,
        module='investment', type_='wizard')
