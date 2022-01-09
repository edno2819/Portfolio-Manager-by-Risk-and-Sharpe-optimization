from scipy.optimize import minimize
import matplotlib.pyplot as plt
import yfinance as yf
from portfolio import *
import numpy  as np
import seaborn as sns


COLORS = ['red','blue','skyblue','orange', 'green',]
sns.set_style('darkgrid', {'legend.frameon':True})
INTERVAL = {'5 Dias':'5d','1 Semana':'1wk','1 Mês':'1mo','3 Mêses':'3mo'}



def set_assets_portfolio(port, assets, start, end, interval):
    data = yf.download(assets, start=start, end=end, interval=interval)
    CLOSES = data['Adj Close']
    port.dates =  list(CLOSES.dropna().index)
    assets_name = list(CLOSES.columns)
    


    for asset in assets_name:
        data =  np.array(list(CLOSES[asset].array))
        data = data[np.logical_not(np.isnan(data))]
        if len(data)>0:
            port.add_asset(asset, data)
            port.assets_dates[asset] = list(CLOSES[asset].dropna().index)

    port.set_max_datas()
    port.set_to_calculate_risk()
    port.calculate_return()

def minimize_portfolio(port):
    assets_name = list(port.port.keys())
    limites = tuple([(0, 1) for c in range(len(assets_name))])
    x0 = [1/len(assets_name) for c in range(len(assets_name))]

    cons = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})
    result = minimize(port.sharpe_ratio_invert, x0, method='SLSQP', bounds=limites, constraints=cons)

    if result.success:
        fitted_params = result.x
        print('\n')
        for asset in range(len(assets_name)):
            print(f"Ação {assets_name[asset]} {round(fitted_params[asset]*100,2)}%")
        print('\n')
        print(f'Risco do portifólio: {round(port.risk_portfolio(fitted_params),3)}%')
        print(f'Retorno do portifólio: {round(port.return_portfolio(fitted_params),3)}%')
        print(f'Indici Sharpe do portifólio: {round(port.sharpe_ratio(fitted_params, risk_free_rate=0.006),3)}')
        print('\n')
    else:
        raise ValueError(result.message)

    return {asse:round(taxa*100,2) for asse, taxa  in zip(assets_name,fitted_params)}, fitted_params

start = "2009-01-01"
end = "2015-04-30"
interval="3 Mêses"
assets = "SPY AAPL FB VALE MSFT VALE ITUB UNH BAC CCL DVN MU"
port = Portifolio()
assets_name = set_assets_portfolio(port, assets, start, end, INTERVAL[interval])
port.portifolio_set(interval)

print(f'Usando o intervalo de {interval} para cálculo do Sharpe Ratio')
fitted_params, taxas_assets = minimize_portfolio(port)

port.circle_chart_portifolio(fitted_params)
port.chart_to_portfolio()
port.chart_to_portfolio_return_porcent(taxas_assets)
port.chart_to_portfolio_return_porcent_2(taxas_assets)


start = "2015-04-30"
end = "2021-10-30"
interval="3 Mêses"
port_teste = Portifolio()

assets_name = set_assets_portfolio(port_teste, assets, start, end, INTERVAL[interval])
port.portifolio_set(interval)

port_teste.chart_to_portfolio()
port_teste.chart_to_portfolio_return_porcent(taxas_assets)