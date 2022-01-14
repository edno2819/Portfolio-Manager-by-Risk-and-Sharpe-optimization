from dash_table import FormatTemplate, DataTable
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from selectionPortfolio import Figs
from dash import html
from app import app
import dash


money = FormatTemplate.money(5)


graph_card = dbc.Card(
    [   html.Button('AtualizarTable', id='Atualizar', n_clicks=0),
        html.Hr(),
        dbc.CardBody(
            [
                html.H4("Gráfico de recorrência de temas", className="card-title", style={"text-align": "center"}),
                DataTable(
                    page_current= 0,
                    page_size= 50,
                    merge_duplicate_headers=True,
                    id='datatable',

                    data=[],
                    columns=[],
                    css=[{
                        'selector': '.dash-spreadsheet td div',
                        'rule': '''
                            line-height: 15px;
                            max-height: 30px; min-height: 30px; height: 30px;
                            display: block;
                            overflow-x: hidden;
                            overflow-y: hidden;
                        '''
                    }],

                    style_header={
                        'fontSize':15,
                        'font-family':'sans-serif',
                        'border': '1px solid grey'
                    },
                    style_data={
                        'whiteSpace': 'normal',
                    },

                    style_cell={'textAlign': 'center',},
                    style_table={'height': '500px', 'overflowY': 'auto', 'border': '1px solid black' },
                )
            ]
        ),
    ],
    color="light",
)
 

# *********************************************************************************************************
datatable_layout = html.Div([
    dbc.Row([dbc.Col(graph_card, width=12)], justify="around")
])
# *********************************************************************************************************

@app.callback(
    Output("datatable", "data"),
    Output("datatable", "columns"),
    Input("AtualizarTable", "n_clicks"), 
)
def update_graph_temas(n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'n_clicks' in changed_id:
        df = Figs.dataset
        df = df['Adj Close'].dropna()
        dates =  list(df.index.values)
        dates = [d.__str__()[:10] for d in dates]

        columns = [{'id': c, 'name': ['Fechamento', c], 'format':money} for c in df.columns]
        columns.insert(0,{"name": ["", "Data"], "id": "Data"})

        data_init = df.to_dict('records')
        for row, date in zip(data_init, dates):
            row['Data'] = date

        return data_init, columns

    return dash.no_update

