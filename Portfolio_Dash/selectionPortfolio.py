from utils.setPortfolio import *


start = "2009-01-01"
end = "2015-04-30"
interval="3 Mêses"
assets = "SPY AAPL FB VALE MSFT VALE ITUB UNH BAC CCL DVN MU"

GrapPor, GrapPor_extra, risco, retorno, sharpe_ratio = createPortfolio(assets, interval, start, end)