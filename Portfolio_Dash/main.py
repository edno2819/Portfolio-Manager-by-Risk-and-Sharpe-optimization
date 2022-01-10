import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from app import app
from selectionPortfolio import *

server = app.server

dados_port = [
    dbc.Col(html.Div([
        html.H5(children='Risco do portifólio', style={'text-align': 'center', 'color': 'red'}),
        html.P(str(risco),style={'text-align': 'center', 'color': 'red', 'fontSize':40})
    ], className='Divhead')),

    dbc.Col(html.Div([
        html.Div([
            html.H5(children='Retorno do portifólio',
            style={'text-align': 'center', 'color': 'green'})
        ]),
        html.P(str(retorno),style={'text-align': 'center', 'color': 'green', 'fontSize':40}),
    ], className='Divhead')),

    dbc.Col(html.Div([
        html.Div([
            html.H5(children='Sharpe-Ratio do portifólio',
            style={'text-align': 'center', 'color': 'blue'})
        ]),
        html.P(str(sharpe_ratio), style={'text-align': 'center', 'color': 'blue', 'fontSize':40}),
    ], className='Divhead'))
]

child = dbc.Container(
    [
        dbc.Row([

            dbc.Col([
            html.H5('Comparativo do Retorno do Portifólio no Periodo Extrapolado(%)', className='text-center'),
            dcc.Graph(id='chat_portfolio_return', style={'height':550}, figure=GrapPor_extra.returnPortfolio()) ],
            width={'size': 8, 'offset': 0, 'order': 1}),

            dbc.Col([
            html.H5('Portfolio', className='text-center'),
            dcc.Graph(id='indicators-ptf',
                      figure=GrapPor.indicatorPeriod(),
                      style={'height':550}),
            ],
            width={'size': 2, 'offset': 0, 'order': 2}),

            dbc.Col([
            html.H5('S&P500', className='text-center'),
            dcc.Graph(id='indicators-sp',
                      figure=GrapPor.indicatorPeriod(),
                      style={'height':550}),
            ],
            width={'size': 2, 'offset': 0, 'order': 3}),
        ]),
        html.Hr(),

        dbc.Row([
            dbc.Col([
                html.H5('Retorno Periódico (%)', className='text-center'),
                dcc.Graph(id='chrt-portfolio-secondary',
                      figure = GrapPor_extra.returnPeriod(),
                      style={'height':420}),
            ],
                width={'size': 8, 'offset': 0, 'order': 1}),
            dbc.Col([
                html.H5('Frações dos Ativos', className='text-center'),
                dcc.Graph(id='pie-top15',
                      figure = GrapPor.circle_chart_portifolio(),
                      style={'height':380}),
            ],
                width={'size': 4, 'offset': 0, 'order': 2}),
        ]),
        html.Hr(),

        dbc.Row([
            dbc.Col([
            html.H5('Valor dos Ativos Selecionados($USD)', className='text-center'),
            dcc.Graph(id='chrt-portfolio-main',
                      figure=GrapPor_extra.chart_to_portfolio(),
                      style={'height':550}),
            ],
                width={'size': 7, 'offset': 0, 'order': 1}),

            dbc.Col([
            html.H5('Fronteira Eficiente', className='text-center'),
            dcc.Graph(id='fronteira-eficiente',
                      figure=GrapPor.fronteiraEficiente(),
                      style={'height':550}),
            ],
            width={'size': 5, 'offset': 0, 'order': 2}),
        ])
        
    ], 
    fluid=False)


app.layout = dbc.Container([
    html.Hr(),
    html.Div(html.Img(src=r'assets\portfolio-png.png', style={'height':'60px', 'width':'70px'}), style={"textAlign": "center"}),
    dbc.Row(dbc.Col(html.H1("Portfolio Análise", style={"textAlign": "center"}), width=12)),
    html.Hr(),
    dbc.Row(dados_port, className="mb-3"),
    dbc.Row(child),
    html.Div(id='content', children=[]),
    html.Br(),
    html.H1("DashBoard para TCC", style={"textAlign": "right"})

    ],className='containerMain')


if __name__=='__main__':
    app.run_server(debug=True)