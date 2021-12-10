from itertools import combinations
import matplotlib.pyplot as plt




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

def datas_to_porcent_init(closes:list):
    new_list = []
    for n in range(1, len(closes)):
        new_list.append(porcent_dif(closes[0], closes[n]))
    return new_list


class Portifolio:
    def __init__(self) -> None:
        self.port = {}
        self.port_porcent = {}
        self.assets_var = {}
        self.assets_cov = {}
        self.assets_return = {}
        self.assets_dates = {}
        self.dates = []


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

    
    def risk_portfolio(self, porcent:list):
        porcent = self.taxas_to_dict(porcent)
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


    def return_portfolio(self, porcent:list, tipo=False):
        porcent = self.taxas_to_dict(porcent)
        retu = 0
        for asset in porcent.keys(): 
            retu += porcent[asset] * self.assets_return[asset]

        return retu if tipo else 1 - retu
    

    def set_to_calculate_risk(self):
        self.calculate_var()
        self.calculate_cov()


    def taxas_to_dict(self, propor:list):
        assets_name = list(self.port.keys())
        taxas = {assets_name[asset]:propor[asset] for asset in range(len(assets_name))}
        return taxas


    def sharpe_ratio(self, porcent, risk_free_rate=0.04, tipo=False):
        standart_deviation = self.risk_portfolio(porcent)
        return_portfolio = self.return_portfolio(porcent, True)
        result = (return_portfolio - risk_free_rate) / standart_deviation
        return result if tipo else 1 - result

    def calculate_por_period(self, porcent, period_size:int):
        result = 0
        for c in range(period_size,len(list(porcent.keys()))-1):
            #lisa[c-period_size:period_size]
            self.set_to_calculate_risk()
            self.calculate_return()
            result += self.sharpe_ratio(porcent)
        return result
    
    def calculate_return_portfolio(self, porcent):
        porcent = self.taxas_to_dict(porcent)
        result = []
        for c in range(len(self.dates)):
            sum = 0
            for asset in porcent.keys(): 
                sum += porcent[asset] * self.port[asset][c]
            result.append(sum)
        return [x+1 for x in datas_to_porcent_init(result)] 

    def chart_to_portfolio_return_porcent(self, taxas):
        with plt.style.context('Solarize_Light2'):
            values = [1]
            values += self.calculate_return_portfolio(taxas)  
            for c in range(len(self.port.keys())): 
                asset = list(self.port.keys())[c]
                plt.plot(self.dates[0], [min(values)], label=f'{asset}:{round(taxas[c]*100,2)}%')

            plt.plot(self.dates, values)
            plt.title('Ações')
            plt.legend(loc="upper left")
            plt.xlabel('Periodo', fontsize=14)
            plt.ylabel('Porcentagem', fontsize=14)
            plt.show()

    def chart_to_portfolio(self):
        with plt.style.context('Solarize_Light2'):
            for asset in self.port.keys():  
                plt.plot(self.assets_dates[asset], self.port[asset], label=asset)

            plt.title('Ações')
            plt.legend(loc="upper left")
            plt.xlabel('x label', fontsize=14)
            plt.ylabel('y label', fontsize=14)
            plt.show()




# import matplotlib.pyplot as plt
# import yfinance as yf
# import numpy  as np

# def set_assets_portfolio(port, assets, start, end, interval):
#     data = yf.download(assets, start=start, end=end, interval=interval)
#     CLOSES = data['Adj Close']
#     port.dates =  list(CLOSES.dropna().index)
#     assets_name = list(CLOSES.columns)
    


#     for asset in assets_name:
#         data =  np.array(list(CLOSES[asset].array))
#         data = data[np.logical_not(np.isnan(data))]
#         if len(data)>0:
#             port.add_asset(asset, data)
#             port.assets_dates[asset] = list(CLOSES[asset].dropna().index)

#     port.set_to_calculate_risk()
#     port.calculate_return()

# start = "2015-04-30"
# end = "2021-04-30"
# interval="3mo"
# assets = "SPY AAPL FB VALE MSFT"
# port_teste = portifolio()

# assets_name = set_assets_portfolio(port_teste, assets, start, end, interval)
# port_teste.chart_to_portfolio([.25,.25,.25,.25,.25])
