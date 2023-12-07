# -*- coding: utf-8 -*-
# This file is part of the investment-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from string import Template
import requests
import logging
import html2text
import re
from datetime import datetime
from decimal import Decimal
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool
from trytond.pyson import Eval, Bool
from trytond.i18n import gettext
from trytond.exceptions import UserError
logger = logging.getLogger(__name__)


sel_rgxdecimal = [
        ('.', '.'),
        (',', ','),
    ]


sel_rgxidtype = [
        ('isin', 'ISIN'),
        ('nsin', 'NSIN'),
        ('symbol', 'Symbol'),
    ]

sel_rgxdatefmt = [
        ('%d.%m.%Y', 'dd.mm.yyyy'),
        ('%d.%m.%y', 'dd.mm.yy'),
        ('%m/%d/%Y', 'mm/dd/yyyy'),
        ('%m/%d/%y', 'mm/dd/yy'),
        ('%Y-%m-%d', 'yyyy-mm-dd'),
        ('%b %d %Y', 'mon dd yyyy'),
    ]

fields_check = [
    'url', 'nsin', 'isin', 'symbol', 'text', 'http_state',
    'fnddate', 'fndrate', 'fndident']


STATES_WEB = {
    'invisible': Eval('query_method', '') != 'web',
    'required': Eval('query_method', '') == 'web',
    }
DEPENDS_WEB = ['query_method']


class OnlineSource(ModelSQL, ModelView):
    'Online Source'
    __name__ = 'investment.source'

    name = fields.Char(string='Name', required=True)
    query_method = fields.Selection(
        string='Method', required=True,
        help='Select the method to retrieve the data.',
        selection='get_query_methods')
    url = fields.Char(string='URL', states=STATES_WEB, depends=DEPENDS_WEB)
    fixed_url = fields.Boolean(
        string='Fixed URL',
        states={
            'invisible': Eval('query_method', '') != 'web',
        }, depends=DEPENDS_WEB,
        help='URL must be defined at investment record.')
    nohtml = fields.Boolean(
        string='Remove HTML',
        help='Removes HTML tags before the text is interpreted.',
        states={
            'invisible': STATES_WEB['invisible'],
        }, depends=DEPENDS_WEB)
    rgxdate = fields.Char(
        string='Date',
        help='Regex code to find the date in the downloaded HTML file.',
        states=STATES_WEB, depends=DEPENDS_WEB)
    rgxdatefmt = fields.Selection(
        string='Date format', selection=sel_rgxdatefmt,
        states=STATES_WEB, depends=DEPENDS_WEB)
    rgxrate = fields.Char(
        string='Rate',
        help='Regex code to find the rate in the downloaded HTML file.',
        states=STATES_WEB, depends=DEPENDS_WEB)
    rgxdecimal = fields.Selection(
        string='Decimal Separator',
        help='Decimal separator for converting the market ' +
        'value into a number.',
        selection=sel_rgxdecimal, states=STATES_WEB, depends=DEPENDS_WEB)
    rgxident = fields.Char(
        string='Identifier',
        help='Regex code to find the identifier in the downloaded HTML file.',
        states={
            'invisible': STATES_WEB['invisible'],
        }, depends=DEPENDS_WEB)
    rgxidtype = fields.Selection(
        string='ID-Type', selection=sel_rgxidtype,
        help='Type of identifier used to validate the result.',
        states={
            'required': Bool(Eval('rgxident', '')),
            'invisible': STATES_WEB['invisible'],
        }, depends=DEPENDS_WEB+['rgxident'])

    # field to test requests
    used_url = fields.Function(fields.Char(
        string='Used URL', readonly=True,
        help='This URL is used to retrieve the HTML file.',
        states={'invisible': STATES_WEB['invisible']}, depends=DEPENDS_WEB),
        'on_change_with_used_url')
    nsin = fields.Function(fields.Char(
        string='NSIN'), 'on_change_with_nsin', setter='set_test_value')
    isin = fields.Function(fields.Char(
        string='ISIN'), 'on_change_with_isin', setter='set_test_value')
    symbol = fields.Function(fields.Char(
        string='Symbol'), 'on_change_with_symbol', setter='set_test_value')
    http_state = fields.Function(fields.Char(
        string='HTTP-State',
        readonly=True), 'on_change_with_http_state')
    text = fields.Function(fields.Text(
        string='Result', readonly=True), 'on_change_with_text')
    fnddate = fields.Function(fields.Date(
        string='Date', readonly=True,
        help='Date found during test query.'),
        'on_change_with_fnddate')
    fndrate = fields.Function(fields.Numeric(
        string='Rate', readonly=True,
        help='Rate found during test query.', digits=(16, 4)),
        'on_change_with_fndrate')
    fndident = fields.Function(fields.Char(
        string='Identifier', readonly=True,
        help='Identifier found during test query.'),
        'on_change_with_fndident')

    @classmethod
    def __setup__(cls):
        super(OnlineSource, cls).__setup__()
        cls._order.insert(0, ('name', 'DESC'))

    @classmethod
    def default_query_method(cls):
        """ default: web
        """
        return 'web'

    @classmethod
    def default_url(cls):
        """ defaul-url
        """
        return 'https://'

    @classmethod
    def default_rgxdate(cls):
        """ code to find date: dd.mm.yyyy
        """
        return '(\\d{2}\\.\\d{2}\\.\\d{4})'

    @classmethod
    def default_rgxdatefmt(cls):
        """ dd.mm.yyyy
        """
        return '%d.%m.%Y'

    @classmethod
    def default_rgxrate(cls):
        """ nn,nn
        """
        return '(\\d+,\\d+)'

    @classmethod
    def default_rgxidtype(cls):
        """ isin
        """
        return 'isin'

    @classmethod
    def default_rgxdecimal(cls):
        """ comma
        """
        return ','

    @classmethod
    def default_nohtml(cls):
        """ default: True
        """
        return True

    @classmethod
    def default_fixed_url(cls):
        """ default: False
        """
        return False

    @fields.depends(*fields_check)
    def on_change_nsin(self):
        """ run request
        """
        self.call_online_source()

    @fields.depends(*fields_check)
    def on_change_isin(self):
        """ run request
        """
        self.call_online_source()

    @fields.depends(*fields_check)
    def on_change_symbol(self):
        """ run request
        """
        self.call_online_source()

    def on_change_with_fnddate(self, name=None):
        return None

    def on_change_with_fndrate(self, name=None):
        return None

    def on_change_with_fndident(self, name=None):
        return ''

    def on_change_with_http_state(self, name=True):
        return ''

    def on_change_with_text(self, name=None):
        return ''

    def on_change_with_nsin(self, name=None):
        return ''

    def on_change_with_isin(self, name=None):
        return ''

    def on_change_with_symbol(self, name=None):
        return ''

    @fields.depends('url', 'isin', 'nsin', 'symbol', 'fixed_url')
    def on_change_with_used_url(self, name=None):
        """ get url for testing
        """
        if self.url:
            return self.get_url_with_parameter(
                isin=self.isin,
                nsin=self.nsin,
                symbol=self.symbol,
                url=self.url,
                )

    @classmethod
    def get_query_methods(cls):
        """ get list of query-methods
        """
        return [
            ('web', gettext('investment.msg_querytype_web')),
            ]

    @classmethod
    def set_test_value(cls, record, name, value):
        """ dont store it
        """
        pass

    @classmethod
    def run_query_method(cls, osource, isin, nsin, symbol, url, debug=False):
        """ run selected query to retrive data
            result: {
                'text': raw-text from query - for debug,
                'http_state': state of query,
                'date': date() if success,
                'rate': Decimal() if success,
                'code': identifier - isin/nsin/symbol
                }
        """
        OSourc = Pool().get('investment.source')

        if getattr(osource, 'query_method', None) == 'web':
            return OSourc.read_from_website(
                osource,
                isin=isin,
                nsin=nsin,
                symbol=symbol,
                debug=debug,
                url=url,
                )

    def call_online_source(self):
        """ use updated values to call online-source,
            for testing parameters
        """
        OSourc = Pool().get('investment.source')

        result = OSourc.run_query_method(
            self, self.isin, self.nsin, self.url,
            self.symbol, debug=True)
        if result is not None:
            self.text = result.get('text', None)
            self.http_state = result.get('http_state', None)
            self.fnddate = result.get('date', None)
            self.fndrate = result.get('rate', None)
            self.fndident = result.get('code', None)

    def get_url_with_parameter(
            self, isin=None, nsin=None, symbol=None, url=None):
        """ generate url
        """
        if self.fixed_url is True:
            if url is None:
                raise UserError(gettext(
                    'investment.msg_missing_url',
                    oname=self.rec_name,
                    ))
            return url
        else:
            if self.url:
                return Template(self.url).substitute({
                      'isin': isin if isin is not None else '',
                      'nsin': nsin if nsin is not None else '',
                      'symbol': symbol if symbol is not None else '',
                  })

    @classmethod
    def update_rate(cls, asset):
        """ read data from inet, write result to rates of asset
        """
        pool = Pool()
        Rate = pool.get('investment.rate')
        IrDate = pool.get('ir.date')

        if len(asset.updtsources) == 0:
            return

        for updtsource in asset.updtsources:
            rate_data = cls.run_query_method(
                    updtsource,
                    isin=asset.isin,
                    nsin=asset.wkn,
                    symbol=asset.secsymb,
                    url=asset.updturl,
                    )

            if len(updtsource.rgxident or '') > 0:
                # check result - same code?
                code = rate_data.get('code', None)
                if code:
                    asset_code = getattr(asset, {
                            'isin': 'isin',
                            'nsin': 'wkn',
                            'symbol': 'secsymb',
                        }[updtsource.rgxidtype])
                    if (asset_code or '').lower() != code.lower():
                        # fail
                        logger.warning(
                            'update_rate: got wrong code ' +
                            '"%(wrong)s" - expected "%(exp)s"' % {
                                'exp': asset_code,
                                'wrong': code,
                                })
                        continue

            to_create = {
                'date': rate_data.get('date', None),
                'rate': rate_data.get('rate', None),
                'asset': asset.id,
                }
            if (to_create['date'] is not None) and \
                    (to_create['rate'] is not None):
                # check if exists
                if Rate.search_count([
                        ('asset.id', '=', asset.id),
                        ('date', '=', to_create['date'])]) == 0:
                    Rate.create([to_create])
                    return True
                else:
                    # if we got a record for today  - stop
                    # otherwise try next source
                    if to_create['date'] == IrDate.today():
                        break
        return False

    def get_regex_result(self, html_text, field_name):
        """ run regex on html-text, convert result
        """
        rgxcode = getattr(self, field_name) or ''
        if len(rgxcode) == 0:
            return None

        search_result = re.compile(rgxcode).search(html_text)
        if search_result is None:
            return None

        try:
            result = search_result.group(1)
        except IndexError:
            result = search_result.group(0)

        if field_name == 'rgxrate':
            dec_sep = [',', '.']
            dec_sep.remove(self.rgxdecimal)

            result = result.replace(
                dec_sep[0], '').replace(self.rgxdecimal, '.')
            try:
                result = Decimal(result)
            except Exception:
                result = None
        elif field_name == 'rgxdate':
            try:
                result = datetime.strptime(result, self.rgxdatefmt).date()
            except Exception:
                result = None
        return result

    @classmethod
    def read_from_website(
            cls, updtsource, isin=None, nsin=None,
            symbol=None, url=None, debug=False):
        """ read from url, extract values
        """
        result = {}

        if updtsource.url == 'https://':
            result['text'] = 'invalid url'
            return result

        res1 = requests.get(
            updtsource.get_url_with_parameter(
                isin=isin,
                nsin=nsin,
                symbol=symbol,
                url=url,
                ),
            allow_redirects=True,
            timeout=5.0)

        result['http_state'] = '%(code)d: %(msg)s' % {
                'code': res1.status_code,
                'msg': res1.reason,
            }

        if res1.status_code in [200, 204]:
            html = res1.text

            # remove html-tags
            if updtsource.nohtml:
                o1 = html2text.HTML2Text()
                o1.ignore_links = True
                o1.ignore_tables = True
                o1.bypass_tables = False
                o1.single_line_break = True
                o1.body_width = 0
                html = o1.handle(html)
                del o1

            if debug:
                result['text'] = html

            result['rate'] = updtsource.get_regex_result(html, 'rgxrate')
            result['date'] = updtsource.get_regex_result(html, 'rgxdate')
            result['code'] = updtsource.get_regex_result(html, 'rgxident')
        else:
            logger.error(
                'read_from_website: ' +
                '%(code)s, url: %(url)s, redirects: [%(redirects)s]' % {
                    'code': res1.status_code,
                    'url': res1.url,
                    'redirects': ', '.join([x.url for x in res1.history]),
                })
            if debug:
                result['text'] = res1.text
        return result

# end OnlineSource
