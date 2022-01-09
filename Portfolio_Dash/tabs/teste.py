import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import dcc
from componetes import *
from app import app


SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '12rem',
    'padding': '2rem 1rem',
    'background-color': 'lightgray',
}
CONTENT_STYLE = {
    'margin-left': '15rem',
    'margin-right': '2rem',
    'padding': '2rem' '1rem',
}

child = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H2('PORTFOLIO OVERVIEW', className='text-center text-primary, mb-3'))),
        dbc.Row([
            dbc.Col([
            html.H5('Total Portfolio Value ($USD)', className='text-center'),
            dcc.Graph(id='chrt-portfolio-main',
                      #figure=chart_ptfvalue,
                      figure=indicators_sp500,
                      style={'height':550}),
            html.Hr(),

            ],
                width={'size': 8, 'offset': 0, 'order': 1}),
            dbc.Col([
            html.H5('Portfolio', className='text-center'),
            dcc.Graph(id='indicators-ptf',
                      #figure=indicators_ptf,
                      figure=indicators_sp500,
                      style={'height':550}),
            html.Hr()
            ],
                width={'size': 2, 'offset': 0, 'order': 2}),
            dbc.Col([
            html.H5('S&P500', className='text-center'),
            dcc.Graph(id='indicators-sp',
                      figure=indicators_sp500,
                      style={'height':550}),
            html.Hr()
            ],
                width={'size': 2, 'offset': 0, 'order': 3}),
        ]),  # end of second row
        dbc.Row([
            dbc.Col([
                html.H5('Monthly Return (%)', className='text-center'),
                dcc.Graph(id='chrt-portfolio-secondary',
                      figure=indicators_sp500,
                      #figure=fig_growth2,
                      style={'height':380}),
            ],
                width={'size': 8, 'offset': 0, 'order': 1}),
            dbc.Col([
                html.H5('Top 15 Holdings', className='text-center'),
                dcc.Graph(id='pie-top15',
                      figure = donut_top,
                      style={'height':380}),
            ],
                width={'size': 4, 'offset': 0, 'order': 2}),
        ])
        
    ], fluid=True)

sidebar = html.Div( 
    [
        html.H5("Navigation Menu", className='display-6'),
        html.Hr(),
        html.P('Navigation Menu', className='text-center'),
        
        dbc.Nav(
            [
                dbc.NavLink('Home', href="/", active='exact'),
                dbc.NavLink('Page2', href="/page-2", active='exact')
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id='page-content', children=child, style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id='url'), sidebar, content])

app.run_server(debug=True)