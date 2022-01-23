import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html
from app import app
import dash_core_components as dcc

import dash
from datetime import date, datetime, timedelta
import utils.variaveis as var
from selectionPortfolio import Figs



image_card = dbc.Card(
    [
        dbc.CardBody(
            [   
                html.H4("Filtros"),
                html.Hr(),

                html.H6("intervalo de busca:", className="card-text"),
                dcc.DatePickerRange(
                    month_format='D/MM/Y',
                    display_format='D/MM/Y',
                    id='date-range',
                    min_date_allowed= date(2005, 1, 1),
                    max_date_allowed= date(2021, 4, 1),
                    initial_visible_month= date(2010, 1, 1),
                    start_date= date(2013, 5, 1),
                    end_date= date(2021, 4, 1),
                ),

                html.Hr(),
                html.H6("tamanho de cada Tick:", className="card-text"),
                dcc.Dropdown(
                            options=[{'label':key, 'value':key} for key in var.INTERVAL.keys()],
                            placeholder="intervalo",
                            id='interval'
                        ),
                html.Hr(),

                dbc.Row([
                    dbc.Col([
                        html.H6("Intervalo de Atualização:", className="card-text"),
                        dcc.Input(id="atualization", type="number", placeholder="input with range",min=1, max=1000, step=1, value=6)
                        ]),
                    dbc.Col([
                        html.H6("Intervalo dos Cálculos:", className="card-text"),
                        dcc.Input(id="dates_to_calculate", type="number", placeholder="input with range",min=5, max=500, step=1, value=52)
                        ])
                    ], justify="around"),

                html.Br(),
                html.Hr(),
                html.H6(" Ações:", className="card-text"),
                dcc.Dropdown(id='assets', 
                        options=[{'label':key, 'value':var.ASSETS[key]} for key in var.ASSETS.keys()],
                        multi=True, style={"color": "#000000"},
                        placeholder="Selecione as Ações",),

                html.Hr(),
                html.H6("variável de Otimização:", className="card-text"),
                dcc.RadioItems(
                        options=var.TIPOS_OTIMIZACAO,
                        value='sharpe',
                        labelStyle={'display': 'inline-block', 'padding-right':'18px'},
                        id='optimize',
                        labelClassName='radio'
                    ),
                html.Hr(),
                dcc.Loading(id="ls-loading-1", children=[html.Button('Comfirmar', id='submit-filter', n_clicks=0)], type="default")

            ]
        ),
    ],
    color='rgb(22, 26, 29)',
)

SelectionPortfolio = html.Div([
    dbc.Row([dbc.Col(image_card, width=8)], justify="around")
])

@app.callback(
    Output("submit-filter", "n_clicks"),
    Input("submit-filter", "n_clicks"),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input("interval", "value"),
    Input("atualization", "value"),
    Input("dates_to_calculate", "value"),
    Input("assets", "value"),
    Input("optimize", "value"),
)
def switch_tab(n_clicks, a, b, c, d, e, f, g):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'n_clicks' in changed_id and not None in [a, b, c, d, e, f, g]:
        start = a[:10]
        end = b
        interval=c
        assets = ''
        for key in var.PORTS_MAKED.keys():
            if key in f:
                assets += ' '.join(var.PORTS_MAKED[key])+' '
                f.pop(f.index(key))
        
        assets += ' '.join(f)
        atualization = d
        dates_to_calculate = e
        tipo = g
        Figs.refresh(assets, interval, start, end, atualization, dates_to_calculate, tipo)
        return dash.no_update
    return dash.no_update
