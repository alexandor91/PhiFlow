import inspect
import os
import datetime
import warnings
from os.path import dirname, exists, join, isfile

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import phi
from .dash_app import DashApp


def build_app_details(dashapp):
    assert isinstance(dashapp, DashApp)
    app = dashapp.app
    details = dcc.Markdown("""
## Details

Summary: %s

Traits: %s

Script path: %s

Data path: %s
    """ % (app.summary, app.traits, inspect.getfile(app.__class__), app.scene))
    return details


def build_description(dashapp):
    assert isinstance(dashapp, DashApp)
    app = dashapp.app
    md_src = _description_markdown_src(app.name, app.subtitle)
    return dcc.Markdown(children=md_src, id='info_markdown')


def _description_markdown_src(title, subtitle=''):
    if subtitle is not None and len(subtitle) > 0:
        return """
# %s

---

> **_About this application:_**

%s

---""" % (title, subtitle)
    else:
        return '# %s' % title


def build_phiflow_info(dashapp):
    setup_file = join(dirname(dirname(inspect.getfile(phi))), 'setup.py')
    version = 'unknown'
    if isfile(setup_file):
        try:
            version = os.popen('python %s --version' % setup_file).read()
        except BaseException as exc:
            warnings.warn('Could not get PhiFlow version: %s' % exc)
    return dcc.Markdown(u"""
This application is based on the open-source simulation framework [Φ-Flow](https://github.com/tum-pbs/PhiFlow), version %s.
""" % version)


def build_app_time(dashapp):
    start_time = datetime.datetime.fromtimestamp(dashapp.app.start_time)

    def build_text():
        now = datetime.datetime.now()
        local_timezone = datetime.datetime.now().astimezone().tzinfo
        return 'Application started: %s (Running for %s seconds)' % (start_time.astimezone(local_timezone).ctime(), (now-start_time).seconds)

    layout = html.Div([
        dcc.Markdown(children=build_text(), id='clock-output'),
        dcc.Interval(id='clock', interval=1000)
    ])

    @dashapp.dash.callback(Output('clock-output', 'children'), [Input('clock', 'n_intervals')])
    def update_clock(_):
        return build_text()

    return layout
