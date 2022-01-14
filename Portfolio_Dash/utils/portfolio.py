from itertools import combinations
from utils.math_calculate import *
from utils.variaveis import TAXA_FREE_RATE


class Portifolio:
    def __init__(self) -> None:
        self.port = {}
        self.port_porcent = {}
        self.port_porcent_init = {}
        self.assets_var = {}
        self.assets_cov = {}
        self.assets_return_medio = {}
        self.assets_return = {}
        self.assets_dates = {}
        self.data_range = 0
        self.dates_range = []
        self.interval = ''


    def add_asset(self, name:str, serie_temporal_close:list):
        self.port[name] = serie_temporal_close
        self.port_porcent[name] = datas_to_porcent(serie_temporal_close)
        self.port_porcent_init[name] = datas_to_porcent_init(serie_temporal_close)
        if len(serie_temporal_close)>self.data_range:
            self.data_range = len(serie_temporal_close)
    

    def set_max_datas(self):
        init = 0
        name_max = 'q'
        for c in self.assets_dates.keys():
            if len(self.assets_dates[c])>init:
                init = len(c)
                name_max = c
        self.dates_range = self.assets_dates[name_max]


    def calculate_return(self):
        for asset in self.port.keys():
            self.assets_return_medio[asset] = media_retorno(self.port[asset])
            self.assets_return[asset] = self.port[asset][-1]/self.port[asset][0]


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


    def return_portfolio(self, porcent:list):
        porcent = self.taxas_to_dict(porcent)
        retu = 0
        for asset in porcent.keys(): 
            retu += porcent[asset] * self.assets_return_medio[asset]
        return retu


    def return_portfolio_invert(self, porcent:list):
        return  1 - self.return_portfolio(porcent)
    

    def set_to_calculate_risk(self):
        self.calculate_var()
        self.calculate_cov()


    def taxas_to_dict(self, propor:list):
        assets_name = list(self.port.keys())
        taxas = {assets_name[asset]:propor[asset] for asset in range(len(assets_name))}
        return taxas


    def sharpe_ratio(self, porcent):
        standart_deviation = self.risk_portfolio(porcent)
        return_portfolio = self.return_portfolio(porcent)
        result = (return_portfolio - TAXA_FREE_RATE[self.interval]) / standart_deviation
        return result 


    def sharpe_ratio_invert(self, porcent):
        return  1 - self.sharpe_ratio(porcent)


    def calculate_por_period(self, porcent, period_size:int):
        result = 0
        for _ in range(period_size,len(list(porcent.keys()))-1):
            self.set_to_calculate_risk()
            self.calculate_return()
            result += self.sharpe_ratio(porcent)
        return result
    