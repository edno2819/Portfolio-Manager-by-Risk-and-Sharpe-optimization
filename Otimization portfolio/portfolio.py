from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np




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
        self.assets_return_medio = {}
        self.assets_return = {}
        self.assets_dates = {}
        self.data_range = 0
        self.dates_range = []
        self.COLORS = ['red','blue','skyblue','orange', 'green',]
        self.interval = ''


    def portifolio_set(self, intervalo):
        self.interval = intervalo
        self.set_max_datas()


    def add_asset(self, name:str, serie_temporal_close:list):
        self.port[name] = serie_temporal_close
        self.port_porcent[name] = datas_to_porcent(serie_temporal_close)
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
            retu += porcent[asset] * self.assets_return[asset]
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


    def sharpe_ratio(self, porcent, risk_free_rate=0.006):
        standart_deviation = self.risk_portfolio(porcent)
        return_portfolio = self.return_portfolio(porcent)
        result = (return_portfolio - risk_free_rate) / standart_deviation
        return result 


    def sharpe_ratio_invert(self, porcent, risk_free_rate=0.006):
        return  1 - self.sharpe_ratio(porcent, risk_free_rate)


    def calculate_por_period(self, porcent, period_size:int):
        result = 0
        for _ in range(period_size,len(list(porcent.keys()))-1):
            self.set_to_calculate_risk()
            self.calculate_return()
            result += self.sharpe_ratio(porcent)
        return result
    

    def chart_to_portfolio_return_porcent(self, taxas):
        def calculate_return_portfolio(taxas):
            '''Calculando o crescimento em porcentagem em relação ao intervalo anterior'''
            porcent = self.taxas_to_dict(taxas)
            result = [0]
            for c in range(self.data_range-1):
                count = 0
                for asset in porcent.keys(): 
                    if len(self.port_porcent[asset])>=c+1:
                        count += porcent[asset] * self.port_porcent[asset][c]
                result.append(count)
            return result

        with plt.style.context('Solarize_Light2'):
            values = calculate_return_portfolio(taxas)  
            for c in range(len(self.port.keys())): 
                asset = list(self.port.keys())[c]
                value_asset = round(taxas[c]*100,2)
                if value_asset>=0.01:
                    plt.plot(self.dates_range[0], [min(values)], label=f'{asset}: {value_asset}%')


    def chart_to_portfolio_return_porcent_2(self, taxas):
        def calculate_return_portfolio(taxas):
            '''Calculando o crescimento em porcentagem em relação ao intervalo anterior'''
            porcent = self.taxas_to_dict(taxas)
            result = [0]
            for c in range(self.data_range-1):
                count = 0
                for asset in porcent.keys(): 
                    if len(self.port[asset])>=c+1:
                        data_to_porcent = [0]
                        data_to_porcent += datas_to_porcent_init(self.port[asset])
                        count += porcent[asset] * data_to_porcent[c]
                result.append(count)
            return result

        with plt.style.context('Solarize_Light2'):
            values = calculate_return_portfolio(taxas)  
            for c in range(len(self.port.keys())): 
                asset = list(self.port.keys())[c]
                value_asset = round(taxas[c]*100,2)
                if value_asset>=0.01:
                    plt.plot(self.dates_range[0], [min(values)], label=f'{asset}: {value_asset}%')

            plt.plot(self.dates_range, values)
            plt.title(f'Taxa de Variação - {self.interval}')
            plt.legend(loc="upper left")
            plt.xlabel('Periodo', fontsize=14)
            plt.ylabel('Porcentagem', fontsize=14)
            plt.xticks(rotation=105)
            plt.show()


    def chart_to_portfolio(self):
        with plt.style.context('Solarize_Light2'):
            for asset in self.port.keys():  
                plt.plot(self.assets_dates[asset], self.port[asset], label=asset)

            plt.title('Ações')
            plt.legend(loc="upper left")
            plt.xlabel('Valor da ação', fontsize=14)
            plt.ylabel('Periodo', fontsize=14)
            plt.xticks(rotation=105)
            plt.show()
    

    def circle_chart_portifolio(self, taxas_assets:dict):
        lis = []
        name_lis = []
        for asset in taxas_assets.keys():
            if taxas_assets[asset]>0.01:
                lis.append(taxas_assets[asset])
                name_lis.append(asset)

        #plt.figure(figsize=(20,10))
        my_circle = plt.Circle( (0,0), 0.7, color='white')
        plt.pie(lis, labels=name_lis, colors=[self.COLORS[c] for c in range(len(lis))], autopct='%1.1f%%')
        p=plt.gcf()
        p.gca().add_artist(my_circle)
        plt.title('Dataset de Treino', fontsize=30)
        plt.show()

