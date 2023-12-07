#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This file is part of the currency_ecbrate-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

import csv, os, sys
from argparse import ArgumentParser
from datetime import datetime, date
from decimal import Decimal


try:
    from proteus import Model, config
except ImportError:
    prog = os.path.basename(sys.argv[0])
    sys.exit("proteus must be installed to use %s" % prog)


def read_csv_file(file_name, dec_devider, date_fmt, delimiter):
    """ read file from csv
    """
    result = []

    del_chars = ['.', ',']
    del_chars.remove(dec_devider)
    min_date = None
    max_date = None
    min_rate = None
    max_rate = None

    with open(file_name, 'r', encoding='latin1') as fhdl:
        csv_lines = csv.DictReader(fhdl, dialect='excel', delimiter=delimiter)

        for line in csv_lines:
            try :
                date_val = datetime.strptime(line.get('date', None).strip(), date_fmt).date()
            except :
                raise ValueError('- failed to read column 1 of file, expected date (format: %s)' % date_fmt)

            try :
                rate_val = line.get('rate', None).replace(del_chars[0], '').strip()
                rate_val = Decimal(rate_val.replace(dec_devider, '.'))
            except :
                raise ValueError('- failed to read column 1 of file, expected date (format: %s)' % date_fmt)

            if isinstance(date_val, date) and isinstance(rate_val, Decimal):
                result.append({'date': date_val, 'rate': rate_val})

                # date range
                if max_date is None:
                    max_date = date_val
                else :
                    if max_date < date_val:
                        max_date = date_val

                if min_date is None:
                    min_date = date_val
                else :
                    if min_date > date_val:
                        min_date = date_val

                # rate range
                if max_rate is None:
                    max_rate = rate_val
                else :
                    if max_rate < rate_val:
                        max_rate = rate_val

                if min_rate is None:
                    min_rate = rate_val
                else :
                    if min_rate > rate_val:
                        min_rate = rate_val

            else :
                raise ValueError('- failed to identify row content: %s' % line)

    print('- found %d records' % len(result))
    print('- dates from %s to %s' % (
            min_date.isoformat() if min_date is not None else '-',
            max_date.isoformat() if max_date is not None else '-',
            ))
    print('- rates from %s to %s' % (
            str(min_rate) if min_rate is not None else '-',
            str(max_rate) if max_rate is not None else '-',
            ))
    return (result, max_date, min_date)



def upload_rates(isin, rates_list, max_date, min_date):
    """ generate to_create for rates
    """
    Rate = Model.get('investment.rate')
    Asset = Model.get('investment.asset')

    # get id of asset by isin
    assets = Asset.find([
            ('isin', '=', isin),
        ])
    if len(assets) == 0:
        print('- ISIN %s not found' % isin)
        return

    # get rate in date-range
    rates = Rate.find([
            ('asset.id', '=', assets[0].id),
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
            'asset': assets[0].id,
            'date': rate['date'],
            'rate': rate['rate'],
            })
        done_dates.append(rate['date'])

    if len(to_create) > 0:
        print('- upload %d historical rates...' % len(to_create))
        Rate.create(to_create, context={})
        print('- finished upload')
    else :
        print('- nothing to upload')


def do_import(csv_file, isin, dec_devider, date_fmt, delimiter):
    """ run import
    """
    print('\n--== Import historical asset rates ==--')
    print('- file: %s' % csv_file)
    print('- ISIN: %s' % isin)
    print('- date-format: %s, decimal divider: "%s", delimiter: "%s"' % (date_fmt, dec_devider, delimiter))
    (lines, max_date, min_date) = read_csv_file(csv_file, dec_devider, date_fmt, delimiter)
    upload_rates(isin, lines, max_date, min_date)

    print('--== finish import ==--')


def main(database, config_file, csv_file, dec_devider, date_fmt, isin, delimiter):
    config.set_trytond(database, config_file=config_file)
    with config.get_config().set_context(active_test=False):
        do_import(csv_file, isin, dec_devider, date_fmt, delimiter)


def run():
    parser = ArgumentParser()
    parser.add_argument('-d', '--database', dest='database', required=True)
    parser.add_argument('-c', '--config', dest='config_file', help='the trytond config file')
    parser.add_argument('-f', '--file', dest='csv_file', required=True,
        help='CSV-file to import, should contain two columns: 1. date, 2. numeric, first line must have "date" and "rate"')
    parser.add_argument('-p', '--decimal', default=',', dest='decimal_divider',
        help='decimal divider, defaults to: ,')
    parser.add_argument('-t', '--delimiter', default=';', dest='delimiter',
        help='field delimiter for csv-table, defaults to: ;')
    parser.add_argument('-a', '--dateformat', default='%d.%m.%Y', dest='date_format',
        help='date format like %%d.%%m.%%Y or %%Y-%%m-%%d or similiar')
    parser.add_argument('-i', '--isin', dest='isin', required=True, help='ISIN of the target asset')

    args = parser.parse_args()
    main(args.database, args.config_file, args.csv_file, args.decimal_divider, \
        args.date_format, args.isin, args.delimiter)


if __name__ == '__main__':
    run()
