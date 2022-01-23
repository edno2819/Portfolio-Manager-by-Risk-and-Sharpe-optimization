from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from selectionPortfolio import Figs
from dash import html
from dash import dcc
from app import app
import dash

dados_port = [
    html.Button('Atualizar', id='Atualizar', n_clicks=0),

    html.Hr(),
    dbc.Row(html.Div([
        html.H5(children='Parâmetros', style={'text-align': 'center', 'color': 'red'}),
        html.P('',  id='parametros', style={'text-align': 'center', 'color': 'white', 'fontSize':19})], className='Divhead')),
    html.Hr(),

    dbc.Col(html.Div([
        html.H5(children='Risco do portifólio', style={'text-align': 'center', 'color': 'red'}),
        html.P(Figs.risco, style={'text-align': 'center', 'color': 'red', 'fontSize':40}, id='risco')
    ], className='Divhead')),

    dbc.Col(html.Div([
        html.Div([
            html.H5(children='Retorno do portifólio',
            style={'text-align': 'center', 'color': 'green'})
        ]),
        html.P(Figs.retur,style={'text-align': 'center', 'color': 'green', 'fontSize':40}, id='retorno'),
    ], className='Divhead')),

    dbc.Col(html.Div([
        html.Div([
            html.H5(children='Sharpe-Ratio do portifólio',
            style={'text-align': 'center', 'color': 'blue'})
        ]),
        html.P(Figs.sharpe, style={'text-align': 'center', 'color': 'blue', 'fontSize':40}, id='sharpe'),
    ], className='Divhead'))
]

child = dbc.Container(
    [
        dbc.Row([

            dbc.Col([
            html.H5('Comparativo do Retorno do Portifólio no Periodo Extrapolado(%)', className='text-center'),
            dcc.Graph(id='returnPortfolio', style={'height':550}, figure=Figs.returnPortfolio())],
            width={'size': 8, 'offset': 0, 'order': 1}),

            dbc.Col([
            html.H5('Portfolio', className='text-center'),
            dcc.Graph(id='indicatorPeriod1',
                      figure=Figs.indicatorPeriod(),
                      style={'height':550}),
            ],
            width={'size': 2, 'offset': 0, 'order': 2}),

            dbc.Col([
            html.H5('Portfolio Bruto', className='text-center'),
            dcc.Graph(id='indicatorPeriod2',
                      figure=Figs.indicatorPeriod(),
                      style={'height':550}),
            ],
            width={'size': 2, 'offset': 0, 'order': 3}),
        ]),
        html.Hr(),

        dbc.Row([
            dbc.Col([
                html.H5('Retorno Periódico (%)', className='text-center'),
                dcc.Graph(id='returnPeriod',
                      figure = Figs.returnPeriod(),
                      style={'height':550}),

            ],width={'size': 6, 'offset': 0, 'order': 1}),

            dbc.Col([
                html.H5('Valor dos Ativos Selecionados($USD)', className='text-center'),
                dcc.Graph(id='graphAssets',
                        figure=Figs.graphAssets(),
                        style={'height':550}),
            ],width={'size': 6, 'offset': 0, 'order': 1}),
        ]),
        html.Hr(),
        html.Br(),
        html.H5('Atualizações do Portfólio', className='text-center'),
        dbc.Row([dcc.Slider(
                min=0,
                max=10,
                step=1,
                value=0,
                tooltip={"placement": "bottom", "always_visible": True},
                id='slider-port',
            )]),

        dbc.Row([
            dbc.Col([
                html.H5('Frações dos Ativos', className='text-center'),
                dcc.Graph(id='circle_chart_portifolio',
                      figure =Figs.figPie(),
                      style={'height':450}),

            ],width={'size': 5, 'offset': 0, 'order': 2}),

            dbc.Col([
                html.H5('Fronteira Eficiente', className='text-center'),
                dcc.Graph(id='fronteiraEficiente',
                        figure=Figs.fronteiraEficiente(),
                        style={'height':450}),
            ],
            width={'size': 7, 'offset': 0, 'order': 2}),
        ])
        
    ], 
    fluid=False)


layout_port = [dbc.Row(dados_port, className="mb-3"), dbc.Row(child)]


@app.callback(
    Output("risco", "children"),
    Output("retorno", "children"),
    Output("sharpe", "children"),
    Output("returnPortfolio", "figure"),
    Output("indicatorPeriod1", "figure"),
    Output("indicatorPeriod2", "figure"),
    Output("returnPeriod", "figure"),
    Output("circle_chart_portifolio", "figure"),
    Output("graphAssets", "figure"),
    Output("fronteiraEficiente", "figure"),
    Output("slider-port", "max"),
    Output("slider-port", "marks"),
    Output("parametros", "children"),
    Input("Atualizar", "n_clicks"),
    Input("slider-port", "value"),

)
def update_graph_temas(n_clicks, value):
    no = dash.no_update
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'n_clicks' in changed_id:
        risco = Figs.risco
        retur = Figs.retur
        sharpe = Figs.sharpe
        fig_1 = Figs.returnPortfolio()
        fig_2 = Figs.indicatorPeriod(Figs.GrapPor.port_main_return)
        fig_3 = Figs.indicatorPeriod(Figs.GrapPor.port_comp_return)
        fig_4 = Figs.returnPeriod()
        fig_5 = Figs.figPie()
        fig_6 = Figs.graphAssets()
        fig_7 = Figs.fronteiraEficiente()   
        size = len(Figs.GrapPor.port)
        dic_size =  {i: '{}'.format(i) for i in range(0, size-1)}
        para_str = f'''Tick: {Figs.param['tick']}  |  Cálculo: {Figs.param['dates_to_calculate']}  |  Atualização: {Figs.param['atualization']}  | 
         Otimização: {Figs.param['otimization']}  |  Inicio: {Figs.param['start']}  |  Final: {Figs.param['end']}'''

        return risco, retur, sharpe, fig_1, fig_2, fig_3, fig_4, fig_5, fig_6, fig_7, size, dic_size, para_str
    else:
        fig_6 = Figs.figPie(value)
        fig_7 = Figs.fronteiraEficiente(value)  
        return no, no, no, no, no, no, no, fig_6, no, fig_7, no, no, no



