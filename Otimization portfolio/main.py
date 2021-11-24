from scipy.optimize import minimize
import yfinance as yf
from portfolio import *
import numpy  as np


assets = "SPY AAPL TSLA FB VALE MSFT"
start = "2016-01-01"
end = "2021-04-30"
interval="3mo"

data = yf.download(assets, start=start, end=end, interval=interval)
CLOSES = data['Adj Close']
assets_name = list(CLOSES.columns)

#'OTIMIZAÇÃO RESTRITA NÃO LINEAR'
a = portifolio()

for asset in assets_name:
    data =  np.array(list(CLOSES[asset].array))
    data = data[np.logical_not(np.isnan(data))]
    if len(data)>0:
        a.add_asset(asset, data)

a.set_to_calculate_risk()
a.calculate_return()

limites = tuple([(0, 1) for c in range(len(assets_name))])
x0 = [1/len(assets_name) for c in range(len(assets_name))]

cons = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})

result = minimize(a.sharpe_ratio, x0, method='SLSQP', bounds=limites, constraints=cons)

if result.success:
    fitted_params = result.x
    print('\n')
    for asset in range(len(assets_name)):
        print(f"Ação {assets_name[asset]} {round(fitted_params[asset]*100,2)}%")
    print('\n')
    print(f'Risco do portifólio: {round(a.risk_portfolio(fitted_params),3)}%')
    print(f'Retorno do portifólio: {round(a.return_portfolio(fitted_params, tipo=True),3)}%')
    print(f'Indici SHARPE do portifólio: {round(a.sharpe_ratio(fitted_params, risk_free_rate=0.006, tipo=True),3)}')
    print('\n')
else:
    raise ValueError(result.message)



