import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html
from app import app
import dash_core_components as dcc

import utils.variaveis as var

from tabs.port import layout_port
from tabs.selecao import SelectionPortfolio
#from tabs.msg_table import datatable_layout


server = app.server


app_tabs = html.Div(
    [
        dcc.Tabs(
            [
                dcc.Tab(label="Portfólio Seleção", value="SelectionPortfolio"),
                dcc.Tab(label="Portfólio Análise", value="layout_port"),
                #dcc.Tab(label="Dados dos Ativos", value="datatable_layout"),
            ],
            id="tabs",
            className='custom-tabs-container',
            parent_className='custom-tabs',
        ),
    ]
    
)


app.layout =  dbc.Container([
    html.Hr(),
    html.Div(html.Img(src=r'assets\portfolio-png.png', style={'height':'60px', 'width':'70px'}), style={"textAlign": "center"}),
    dbc.Row(dbc.Col(html.H1("Portfólio Análise", style={"textAlign": "center"}), width=12)),
    html.Hr(),
    dbc.Row(dbc.Col(app_tabs, width=16)),
    html.Hr(),
    html.Div(id='content', children=[]),
    html.Br(),
    html.H1("DashBoard para TCC", style={"textAlign": "right"})

    ],className='containerMain')
 


@app.callback(
    Output("content", "children"),
    Input("tabs", "value"),
)
def switch_tab(tab_chosen): 
    if tab_chosen == "SelectionPortfolio":
        return SelectionPortfolio
    elif tab_chosen == "layout_port":
        return layout_port

    return SelectionPortfolio
        

if __name__=='__main__':
    app.run_server(debug=False)