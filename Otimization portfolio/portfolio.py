from itertools import combinations
import numpy as np 
import yfinance as yf



def covariancia(closes_1, closes_2):
    c = 0
    n = len(closes_1)
    mean_1 = sum(closes_1)/len(closes_1)
    mean_2 = sum(closes_2)/len(closes_2)

    for close_1, close_2 in zip(closes_1, closes_2):
        c += (close_1 - mean_1)*(close_2 - mean_2)
    c /= n - 1
    return c

def variancia(closes):
    v = 0
    mean = sum(closes)/len(closes)
    for close in closes:
        v += (close - mean)**2
    v /= len(closes)-1
    return v

def media_retorno(closes:list):
    mean = 0
    for n in range(1, len(closes)):
        mean += retorno(closes[n], closes[n-1])
    mean /= len(closes)-1
    return mean#ja é em  porcentagem

def retorno(close_now:float, close_before:float):
    return (close_now - close_before)/close_before



def covariancia(closes_1, closes_2):
    c = 0
    n = len(closes_1)
    mean_1 = sum(closes_1)/len(closes_1)
    mean_2 = sum(closes_2)/len(closes_2)

    for close_1, close_2 in zip(closes_1, closes_2):
        c += (close_1 - mean_1)*(close_2 - mean_2)
    c /= n - 1
    return c

def variancia_porcent(closes):
    v = 0
    mean = media_retorno(closes)
    for c in range(1, len(closes)):
        close = closes[c]
        close_before = closes[c-1]
        v += (porcent_dif(close_before, close) - mean)**2
    v /= len(closes)-1
    return v

def porcent_dif(base, new):
    x = (100 * new)/base
    return (x - 100)/100

def datas_to_porcent(closes:list):
    new_list = []
    for n in range(1, len(closes)):
        new_list.append(porcent_dif(closes[n-1], closes[n]))
    return new_list


class portifolio:
    def __init__(self) -> None:
        self.port = {}
        self.port_porcent = {}
        self.assets_var = {}
        self.assets_cov = {}
        self.assets_return = {}

    def add_asset(self, name:str, serie_temporal_close:list):
        self.port[name] = serie_temporal_close
        self.port_porcent[name] = datas_to_porcent(serie_temporal_close)
    
    def calculate_return(self):
        for asset in self.port.keys():
            self.assets_return[asset] = media_retorno(self.port[asset])


    def calculate_var(self):
        for asset in self.port.keys():
            self.assets_var[asset] = variancia(self.port_porcent[asset])

    def calculate_cov(self):
        self.comb = list(combinations(self.port.keys(), 2))

        for asset1, asset2 in self.comb:
            self.assets_cov[asset1+'/'+asset2] = covariancia(self.port_porcent[asset1], self.port_porcent[asset2])

    
    def risk_portfolio(self, porcent:dict):
        risk = []
        for asset in porcent.keys(): 
            risk.append((porcent[asset]**2) * self.assets_var[asset])

        #combinação simples entre os assets
        for asset1, asset2 in self.comb:
            risk.append( 2 * porcent[asset1] * porcent[asset2] * self.assets_cov[asset1+'/'+asset2])

        return sum(risk)**(0.5)

    def risk_portfolio_equal(self):
        risk = []
        simboly = ['x', 'y', 'z', 'p', 'q', 'g', 'm', 'l']
        sym = {list(self.assets_var.keys())[c]:simboly[c] for c in range(len(self.assets_var.keys()))}

        for asset in self.assets_var.keys(): 
            risk.append(f'(({sym[asset]}**2) * {self.assets_var[asset]})')

        #combinação simples entre os assets
        for asset1, asset2 in self.comb:
            risk.append( f"(2 * {sym[asset1]} * {sym[asset2]} * {self.assets_cov[asset1+'/'+asset2]})")

        equal = '(' + ' + '.join(risk) +')**0.5'

        return equal#eval(equal)

    def return_portfolio(self, porcent:dict):
        retu = 0
        for asset in porcent.keys(): 
            retu += porcent[asset] * self.assets_return[asset]

        return retu
    
    def set_to_calculate_risk(self):
        self.calculate_var()
        self.calculate_cov()


# assets = "SPY AAPL TSLA FB"
# start = "2017-01-01"
# end = "2021-04-30"
# interval="1wk"

# data = yf.download(assets, start=start, end=end, interval=interval)
# CLOSES = data['Adj Close']
# assets_name = list(CLOSES.columns)

# a = portifolio()

# for asset in assets_name:
#     data =  np.array(list(CLOSES[asset].array))
#     data = data[np.logical_not(np.isnan(data))]
#     a.add_asset(asset, data)

# a.set_to_calculate_risk()
# a.calculate_return()

# equal = a.risk_portfolio_equal()

# def equal_minimun(propor:list):
#     taxas = {assets_name[asset]:propor[asset] for asset in range(len(assets_name))}

#     print(f'\n\nPORPORÇÕES DE ATIVOS: {taxas}')
#     print(f'The Portfolio Risk: {round(a.risk_portfolio_equal(taxas),4)}%')
#     print(f'Expected Portfolio Return: {round(a.return_portfolio(taxas),4)}%\n')

# equal_minimun([.25, .25, .25, .25])
# equal_minimun([.45, .30, .5, .2])
# equal_minimun([.45, .05, .0, .5])
# equal_minimun([.0, .0, .0, 1])


