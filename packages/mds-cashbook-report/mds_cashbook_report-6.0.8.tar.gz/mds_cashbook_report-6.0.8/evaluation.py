# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields, sequence_ordered
from trytond.pyson import Eval
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.i18n import gettext
from .colors import sel_color as sel_bgcolor
from .templates import template_view_graph, template_view_line, \
    cashbook_types, category_types, booktype_types


sel_chart = [
    ('vbar', 'Vertical Bars'),
    ('hbar', 'Horizontal Bars'),
    ('pie', 'Pie'),
    ('line', 'Line'),
    ]


sel_maincolor = [
    ('default', 'Default'),
    ('red', 'Red'),
    ('green', 'Green'),
    ('grey', 'Grey'),
    ('black', 'Black'),
    ('darkcyan', 'Dark Cyan'),
]


class Evaluation(sequence_ordered(), ModelSQL, ModelView):
    'Evaluation'
    __name__ = 'cashbook_report.evaluation'

    company = fields.Many2One(
        string='Company', model_name='company.company',
        required=True, ondelete="RESTRICT")
    name = fields.Char(string='Name', required=True)
    dtype = fields.Selection(
        string='Data type', required=True, sort=True,
        selection='get_sel_etype', help='Type of data displayed')
    dtype_string = dtype.translated('dtype')
    chart = fields.Selection(
        string='Chart type', required=True, sort=False,
        selection=sel_chart, help='Type of graphical presentation.')
    legend = fields.Boolean(string='Legend')
    maincolor = fields.Selection(
        string='Color scheme', required=True,
        help='The color scheme determines the hue of all ' +
        'components of the chart.', selection=sel_maincolor, sort=False)
    bgcolor = fields.Selection(
        string='Background Color', required=True,
        help='Background color of the chart area.', sort=False,
        selection=sel_bgcolor)
    currency = fields.Many2One(
        string='Currency', ondelete='RESTRICT',
        model_name='currency.currency')

    cashbooks = fields.Many2Many(
        string='Cashbooks', relation_name='cashbook_report.eval_line',
        origin='evaluation', target='cashbook',
        states={'invisible': ~Eval('dtype', '').in_(cashbook_types)},
        depends=['dtype'])
    types = fields.Many2Many(
        string='Types', relation_name='cashbook_report.eval_line',
        origin='evaluation', target='dtype',
        states={'invisible': ~Eval('dtype', '').in_(booktype_types)},
        depends=['dtype'])
    currencies = fields.Many2Many(
        string='Currencies', relation_name='cashbook_report.eval_line',
        origin='evaluation', target='currency',
        filter=[('cashbook_hasbookings', '=', True)],
        states={'invisible': Eval('dtype', '') != 'currencies'},
        depends=['dtype'])
    categories = fields.Many2Many(
        string='Categories', relation_name='cashbook_report.eval_line',
        origin='evaluation', target='category',
        states={'invisible': ~Eval('dtype', '').in_(category_types)},
        depends=['dtype'])

    line_values = fields.One2Many(
        string='Line Values', field='evaluation', readonly=True,
        model_name='cashbook_report.eval_line')

    ui_view_chart = fields.Many2One(
        string='UI View Chart', model_name='ir.ui.view', ondelete='SET NULL')
    dashb_actwin = fields.Many2One(
        string='Dashboard Window', model_name='ir.action.act_window',
        ondelete='SET NULL')
    dashb_actview = fields.Many2One(
        string='Dashboard View', model_name='ir.action.act_window.view',
        ondelete='SET NULL')

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
    def default_bgcolor(cls):
        """ default: Yellow 5
        """
        return '#ffffc0'

    @classmethod
    def default_maincolor(cls):
        """ default: 'default'
        """
        return 'default'

    @classmethod
    def default_legend(cls):
        """ default True
        """
        return True

    @classmethod
    def default_dtype(cls):
        """ default 'book'
        """
        return 'cashbooks'

    @classmethod
    def default_chart(cls):
        """ default 'pie'
        """
        return 'pie'

    @classmethod
    def get_sel_etype(cls):
        """ get list of evaluation-types
        """
        return [
            ('cashbooks', gettext('cashbook_report.msg_dtype_cashbook')),
            ('types', gettext('cashbook_report.msg_dtype_type')),
            ('currencies', gettext('cashbook_report.msg_dtype_currency')),
            ('categories', gettext('cashbook_report.msg_dtype_category')),
            ]

    @classmethod
    def get_create_view_data(cls, evaluation):
        """ generate dictionary to create view-xml
        """
        return {
            'model': 'cashbook_report.eval_line',
            'module': 'cashbook_report',
            'priority': 10,
            'type': 'graph',
            'data': template_view_graph % {
                'bgcol': '' if evaluation.bgcolor == 'default'
                    else 'background="%s"' % evaluation.bgcolor,
                'legend': '1' if evaluation.legend is True else '0',
                'type': evaluation.chart,
                'colscheme': '' if evaluation.maincolor == 'default'
                    else 'color="%s"' % evaluation.maincolor,
                'lines': template_view_line % {
                    'fill': '1',
                    'string': evaluation.dtype_string}}}

    @classmethod
    def uiview_delete(cls, evaluations):
        """ delete action view from evalualtion
        """
        pool = Pool()
        UiView = pool.get('ir.ui.view')
        ActWin = pool.get('ir.action.act_window')

        to_delete_uiview = []
        to_delete_window = []
        for evaluation in evaluations:
            if evaluation.ui_view_chart:
                to_delete_uiview.append(evaluation.ui_view_chart)
            if evaluation.dashb_actwin:
                to_delete_window.append(evaluation.dashb_actwin)

        with Transaction().set_context({
                '_check_access': False}):
            if len(to_delete_uiview) > 0:
                UiView.delete(to_delete_uiview)
            if len(to_delete_window) > 0:
                ActWin.delete(to_delete_window)

    @classmethod
    def uiview_create(cls, evaluations):
        """ create ui view for current setup of evaluation
        """
        pool = Pool()
        UiView = pool.get('ir.ui.view')
        ActWin = pool.get('ir.action.act_window')
        ActView = pool.get('ir.action.act_window.view')
        Evaluation2 = pool.get('cashbook_report.evaluation')
        try:
            DashboardAction = pool.get('dashboard.action')
        except Exception:
            DashboardAction = None

        to_write_eval = []
        to_write_dbaction = []
        for evaluation in evaluations:
            with Transaction().set_context({
                    '_check_access': False}):
                view_graph, = UiView.create([
                    cls.get_create_view_data(evaluation),
                    ])

                dashb_actwin, = ActWin.create([{
                    'name': evaluation.name,
                    'res_model': 'cashbook_report.eval_line',
                    'usage': 'dashboard',
                    'domain': '[["evaluation", "=", %d]]' % evaluation.id,
                    }])

                dashb_actview, = ActView.create([{
                    'sequence': 10,
                    'view': view_graph.id,
                    'act_window': dashb_actwin.id,
                    }])

            to_write_eval.extend([
                [evaluation],
                {
                    'ui_view_chart': view_graph.id,
                    'dashb_actwin': dashb_actwin.id,
                    'dashb_actview': dashb_actview.id,
                }])

            # prepare update dasboard-action
            if DashboardAction is not None:
                if evaluation.dashb_actwin:
                    db_actions = DashboardAction.search([
                        ('act_window.id', '=', evaluation.dashb_actwin.id),
                        ])
                    if len(db_actions) > 0:
                        to_write_dbaction.extend([
                            db_actions,
                            {
                                'act_window': dashb_actwin.id,
                            }])

        if len(to_write_dbaction) > 0:
            DashboardAction.write(*to_write_dbaction)

        cls.uiview_delete(evaluations)

        if len(to_write_eval) > 0:
            Evaluation2.write(*to_write_eval)

    @classmethod
    def create(cls, vlist):
        """ add chart
        """
        records = super(Evaluation, cls).create(vlist)
        cls.uiview_create(records)
        return records

    @classmethod
    def write(cls, *args):
        """ unlink records if dtype changes
        """
        to_write = []
        to_update_uiview = []

        actions = iter(args)
        for evaluations, values in zip(actions, actions):
            # update ui-view if related fields change
            if len(set({
                    'name', 'dtype', 'bgcolor', 'maincolor',
                    'legend', 'chart'}).intersection(values.keys())) > 0:
                to_update_uiview.extend(evaluations)

            # unlink records if dtype changes
            if 'dtype' in values.keys():
                for evaluation in evaluations:
                    if evaluation.dtype == values['dtype']:
                        continue

                    for dt in [
                            'cashbooks', 'types', 'currencies',
                            'categories']:
                        if (not values['dtype'].startswith(dt)) and \
                                (len(getattr(evaluation, dt)) > 0):
                            to_write.extend([
                                [evaluation],
                                {
                                    dt: [('remove', [
                                        x.id for x in getattr(
                                            evaluation, dt)])],
                                }])

        args = list(args)
        args.extend(to_write)
        super(Evaluation, cls).write(*args)

        if len(to_update_uiview) > 0:
            cls.uiview_create(to_update_uiview)

    @classmethod
    def delete(cls, evaluations):
        """ delete views
        """
        cls.uiview_delete(evaluations)
        super(Evaluation, cls).delete(evaluations)

# end Evaluation
