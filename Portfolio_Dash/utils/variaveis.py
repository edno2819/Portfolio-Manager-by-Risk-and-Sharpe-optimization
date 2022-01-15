
# ------------------------- variaveis para a análise ---------------------------------------------------------------------------

TAXA_FREE_RATE = {'5 Dias':0.0012,'1 Semana':0.0015,'1 Mês':0.006,'3 Mêses':0.018}
QTD_RETORNO_PERIODICO = 10
ATIVOS = {'S&P 500': '^GSPC', 'IBOVESPA':'^BVSP'}


# ------------------------- variaveis para a seleção ---------------------------------------------------------------------------

INTERVAL = {'5 Dias':'5d','1 Semana':'1wk','1 Mês':'1mo','3 Mêses':'3mo'}
ASSETS = {
'AAPL':'AAPL','VALE':'VALE','ITUB':'ITUB','BAC':'BAC','BBD':'BBD', 
'TSM':'TSM', 'MU':'MU', 'SPY':'SPY', 'FB':'FB', 'MSFT':'MSFT', 'UNH':'UNH',
'CCL':'CCL', 'DVN':'DVN', 'TNP-PF':'TNP-PF', 'GLOG-PA':'GLOG-PA', 'TAEE11.SA':'TAEE11.SA',
'BBSE3.SA':'BBSE3.SA', 'ENBR3.SA':'ENBR3.SA', 'WEGE3.SA':'WEGE3.SA', 'B3SA3.SA':'B3SA3.SA',
'LREN3.SA':'LREN3.SA'
}
TIPOS_OTIMIZACAO = [{'label': ' Risco', 'value': 'risco'},{'label': ' Retorno', 'value': 'retorno'},{'label': ' Sharpe-Ratio', 'value': 'sharpe'}]


# ------------------------- style ---------------------------------------------------------------------------
COLORS = ['red','blue','skyblue','orange', 'green',]
CHART_THEME = 'plotly_dark'  # others include seaborn, ggplot2, plotly_dark
tabs_styles = {
    'height': '60px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}



