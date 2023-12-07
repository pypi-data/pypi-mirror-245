# -*- coding: utf-8 -*-
# This file is part of the investment-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from io import StringIO
from datetime import datetime, date
from decimal import Decimal
import csv
from trytond.pool import Pool
from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.transaction import Transaction
from trytond.exceptions import UserError
from trytond.i18n import gettext


sel_dec_divider = [
    (',', ','),
    ('.', '.'),
    ]

sel_date_fmt = [
    ('%d.%m.%Y', 'dd.mm.yyyy'),
    ('%Y-%m-%d', 'yyyy-mm-dd'),
    ('%m/%d/%Y', 'mm/dd/yyyy'),
    ]

sel_field_delimiter = [
    (';', ';'),
    (',', ','),
    ]


class ImportWizardStart(ModelView):
    'Import CSV-File'
    __name__ = 'investment.imp_wiz.start'

    asset = fields.Many2One(
        string='Asset', readonly=True, model_name='investment.asset')
    file_ = fields.Binary(string="CSV-File", required=True)
    dec_divider = fields.Selection(
        string='Decimal divider', required=True, selection=sel_dec_divider)
    date_fmt = fields.Selection(
        string='Date format', required=True, selection=sel_date_fmt)
    field_delimiter = fields.Selection(
        string='Field delimiter', required=True, selection=sel_field_delimiter)

# end ImportWizardStart


class ImportWizard(Wizard):
    'Import CSV-File'
    __name__ = 'investment.imp_wiz'

    start_state = 'start'
    start = StateView(
        model_name='investment.imp_wiz.start',
        view='investment.imp_wiz_start_form',
        buttons=[
            Button(string='Cancel', state='end', icon='tryton-cancel'),
            Button(
                string='Import File', state='importf',
                icon='tryton-import', default=True),
            ])
    importf = StateTransition()

    def default_start(self, fields):
        """ show asset
        """
        context = Transaction().context

        values = {
            'dec_divider': ',',
            'date_fmt': '%d.%m.%Y',
            'field_delimiter': ';',
            }
        values['asset'] = context.get('active_id', None)
        return values

    def transition_importf(self):
        """ read file, import
        """
        pool = Pool()
        ImportWiz = pool.get('investment.imp_wiz', type='wizard')

        if self.start.file_ is not None:
            (lines, max_date, min_date) = ImportWiz.read_csv_file(
                    self.start.file_.decode('utf8'),
                    dec_divider=self.start.dec_divider,
                    date_fmt=self.start.date_fmt,
                    delimiter=self.start.field_delimiter)

            if len(lines) > 0:
                ImportWiz.upload_rates(
                    self.start.asset,
                    lines, min_date, max_date)
        return 'end'

    @classmethod
    def upload_rates(cls, asset, rates_list, min_date, max_date):
        """ upload new rates to asset
        """
        Rate = Pool().get('investment.rate')

        # get rate in date-range
        rates = Rate.search([
                ('asset.id', '=', asset.id),
                ('date', '>=', min_date),
                ('date', '<=', max_date),
            ])
        existing_dates = [x.date for x in rates]
        done_dates = []

        to_create = []
        for rate in rates_list:
            if rate['date'] in existing_dates:
                continue
            if rate['date'] in done_dates:
                continue

            to_create.append({
                'asset': asset.id,
                'date': rate['date'],
                'rate': rate['rate'],
                })
            done_dates.append(rate['date'])

        if len(to_create) > 0:
            Rate.create(to_create)

    @classmethod
    def read_csv_file(cls, file_content, dec_divider, date_fmt, delimiter):
        """ read file-content from csv
        """
        result = []

        del_chars = ['.', ',']
        del_chars.remove(dec_divider)
        min_date = None
        max_date = None
        min_rate = None
        max_rate = None

        with StringIO(file_content) as fhdl:
            csv_lines = csv.DictReader(
                fhdl,
                fieldnames=['date', 'rate'],
                dialect='excel',
                delimiter=delimiter)

            for line in csv_lines:
                # skip first line
                if line.get('date', '') == 'date':
                    continue

                try:
                    date_val = datetime.strptime(
                        line.get('date', None).strip(), date_fmt).date()
                except Exception:
                    raise UserError(gettext(
                        'investment.msg_import_err_date',
                        datefmt=date_fmt,
                        colnr='1',
                        ))
                try:
                    rate_val = line.get('rate', None).replace(
                        del_chars[0], '').strip()
                    rate_val = Decimal(rate_val.replace(dec_divider, '.'))
                except Exception:
                    raise UserError(gettext(
                        'investment.msg_import_err_date',
                        datefmt='dd%sdd' % dec_divider,
                        colnr='2'))

                if isinstance(date_val, date) and isinstance(
                        rate_val, Decimal):
                    result.append({'date': date_val, 'rate': rate_val})

                    # date range
                    if max_date is None:
                        max_date = date_val
                    else:
                        if max_date < date_val:
                            max_date = date_val

                    if min_date is None:
                        min_date = date_val
                    else:
                        if min_date > date_val:
                            min_date = date_val

                    # rate range
                    if max_rate is None:
                        max_rate = rate_val
                    else:
                        if max_rate < rate_val:
                            max_rate = rate_val

                    if min_rate is None:
                        min_rate = rate_val
                    else:
                        if min_rate > rate_val:
                            min_rate = rate_val
                else:
                    raise UserError(gettext(
                        'investment.msg_err_unknown_content',
                        linetxt=line))
        return (result, max_date, min_date)

# end ImportWizard
