# -*- coding: utf-8 -*-
# This file is part of the investment-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.wizard import Wizard, StateTransition
from trytond.pool import Pool
from trytond.transaction import Transaction


class UpdateSoureWizard(Wizard):
    'Update Source'
    __name__ = 'investment.source_update'

    start_state = 'runupdate'
    runupdate = StateTransition()

    def transition_runupdate(self):
        """ update selected sources
        """
        pool = Pool()
        OnlineSource = pool.get('investment.source')
        Asset = pool.get('investment.asset')
        context = Transaction().context

        assets = Asset.browse(context.get('active_ids', []))
        to_run_activities = []
        for asset in assets:
            if OnlineSource.update_rate(asset):
                to_run_activities.append(asset)

        if len(to_run_activities) > 0:
            Asset.after_update_actions(to_run_activities)

        return 'end'

# UpdateSoureWizard
