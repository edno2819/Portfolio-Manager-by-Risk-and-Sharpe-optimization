import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from app import app
from datetime import date, datetime, timedelta


image_card = dbc.Card(
    [
        dbc.CardBody(
            [   
                html.H4("Filtros", className="card-title"),
                html.Hr(),

                html.H6("Selecione o intervalo de busca:", className="card-text"),
                html.Br(),
                dcc.DatePickerRange(
                    month_format='D/MM/Y',
                    display_format='D/MM/Y',
                    id='my-date-picker-range',
                    min_date_allowed=date(2021, 1, 5),
                    max_date_allowed=date.today(),
                    initial_visible_month=date.today(),
                    start_date= (datetime.today() - timedelta(days=7)),
                    end_date=date.today(),
                ),

                html.Hr(),
                html.H6("Selecione a palavra chave:", className="card-text"),
                html.Br(),
                dcc.Input(id='word_filter_tema'),
                html.Br(),
                html.Hr(),
                html.H6("Selecione os grupos:", className="card-text"),
                html.Br(),
                html.Br(),
                html.Hr(),
                html.Button('Submit', id='submit-filter', n_clicks=0)
            ]
        ),
    ],
    color="light",
)

graph_card = dbc.Card(
    [   html.Hr(),
        dbc.CardBody(
            [
                html.H4("Gráfico de frequência de temas", className="card-title", style={"text-align": "center"}),
                dcc.Graph(id='line_chart_temas', figure={}),

            ]
        ),
    ],
    color="light",
)
 

# *********************************************************************************************************
frequencia_temas_layout = html.Div([
    dbc.Row([dbc.Col(image_card, width=4), dbc.Col(graph_card, width=8)], justify="around")
])
# *********************************************************************************************************


    
