# -*- coding: utf-8 -*-
# This file is part of the investment-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.


from trytond.tests.test_tryton import ModuleTestCase
from .asset import AssetTestCase
from .rate import RateTestCase
from .source import SourceTestCase
from .wizard import WizardTestCase


class InvestmentTestCase(
        WizardTestCase,
        SourceTestCase,
        RateTestCase,
        AssetTestCase,
        ModuleTestCase):
    'Test investment module'
    module = 'investment'

# end InvestmentTestCase


del ModuleTestCase
