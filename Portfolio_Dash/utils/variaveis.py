
# ------------------------- variaveis para a análise ---------------------------------------------------------------------------
TAXA_FREE_RATE = {'5 Dias':0.0012,'1 Semana':0.0015,'1 Mês':0.006,'3 Mêses':0.018}

QTD_RETORNO_PERIODICO = 10

ATIVOS = {'S&P 500': '^GSPC', 'IBOVESPA':'^BVSP'}

# ------------------------- variaveis para a seleção ---------------------------------------------------------------------------
INTERVAL = {'5 Dias':'5d','1 Semana':'1wk','1 Mês':'1mo','3 Mêses':'3mo'}

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

# ------------------------- PORTFOLIOS SELECIONADOS ---------------------------------------------------------------------------

ASSETS = {
'AAPL':'AAPL','VALE':'VALE','ITAU':'ITUB','BAC':'BAC','BBD':'BBD', 
'TSM':'TSM', 'MU':'MU', 'SPY':'SPY', 'FB':'FB', 'MSFT':'MSFT', 'UNH':'UNH',
'CCL':'CCL', 'DVN':'DVN', 'TAEE11.SA':'TAEE11.SA', 'B3':'B3SA3.SA', 'Commodities':'PDBC',
'USD':'USD', 'REAL/DOLAR':'BRL=X', 'ÓLEO E GÁS':'UKOG.L', 'PRATA':'ZIH22.NYB', 'OURO':'IAU',
'AMBEVE':'ABEV3.SA', 'BB Seguridade':'BBSE3.SA', 'brMalls':'BRML3.SA','Bradesco':'BBDC3.SA','Bradespar':'BRAP4.SA',
'Banco do Brasil':'BBAS3.SA', 'Braskem':'BRKM5.SA', 'BRF':'BRFS3.SA','Grupo CCR':'CCRO3.SA', 'CMIG4':'CMIG4.SA',
'CIELO':'CIEL3.SA', 'Cosan':'CSAN3.SA', 'CYRELA':'CYRE3.SA', 'Eco Rodovias': 'ECOR3.SA', 'Eletrobras':'ELET3.SA',
'EMBRAER':'EMBR3.SA','EDP Brasil':'ENBR3.SA', ' Engie Brasil':'EGIE3.SA', 'EQUATORIAL':'EQTL3.SA', 'Fleury':'FLRY3.SA',
'Gerdau':'GGBR4.SA', 'Metalúrgica Gerdau': 'GOAU4.SA', 'GOL':'GOLL4.SA','Hypera Pharma':'HYPE3.SA','Global Connections':'GC=F',
}

IBOVE = [
'ITUB4.SA',
'BBDC3.SA',
'VALE3.SA',
'PETR3.SA',
'ABEV3.SA',
'BBAS3.SA',
'B3SA3.SA',
'ITSA4.SA',
'LREN3.SA',
'UGPA3.SA',
'BBDC3.SA',
'SUZB3.SA',
'JBSS3.SA',
'RENT3.SA',
'BRFS3.SA',
'BRFS3.SA',
'SANB11.SA',
'EQTL3.SA',
'GGBR4.SA',
'BRKM5.SA',
'EMBR3.SA',
'WEGE3.SA',
'LAME4.SA',
'CMIG4.SA',
'CIEL3.SA',
'RADL3.SA',
'SBSP3.SA',
'BRML3.SA',
'ELET3.SA',
'MULT3.SA',
'CSAN3.SA',
'FLRY3.SA',
'CSNA3.SA',
'BRAP4.SA',
'TAEE11.SA',
'ENBR3.SA',
'USIM5.SA',
'CYRE3.SA',
'MRVE3.SA',
'GOAU4.SA',
'GOLL4.SA',
'QUAL3.SA',
'MRFG3.SA',
'ECOR3.SA',
]

TESTE = ['MRFG3.SA', 'VALE3.SA', 'WEGE3.SA']

CARTEIRA_RISCO = ['PDBC', 'IAU', 'BRL=X'] + IBOVE

PORTS_MAKED = {'IBOVE': IBOVE, 'CARTEIRA RISCO': CARTEIRA_RISCO, 'TESTE ALTA': TESTE}

ASSETS.update({key:key for key in PORTS_MAKED.keys()})