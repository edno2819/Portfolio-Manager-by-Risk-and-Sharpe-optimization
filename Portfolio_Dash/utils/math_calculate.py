import pandas as pd
from statistics import *

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
    variance(closes)
    return  variance(closes)

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

def drawdown_function(return_series: pd.Series):    
    wealth_index = 1*(1+return_series).cumprod()

    pico = wealth_index.cummax()

    drawdowns = (wealth_index - pico)/pico

    pd.DataFrame({'Wealth': wealth_index, 'Pico': pico,'Drawdowns': drawdowns})
    return drawdowns.min() * -100

def max_drawdowm(serie):
    data = {c:serie[c] for c in range(len(serie))}
    data = pd.DataFrame(data.items(), columns=['Date', 'Adj Close'])
    data.dropna()
    data['ret'] = data['Adj Close'].pct_change()

    return drawdown_function(data['ret'])

def superi(a, b):
    count, dif = 0, 0
    count2, dif2 = 0, 0
    for fist, two in zip(a, b):
        if fist>two:
            count+=1
            dif+=fist-two
        elif two>fist:
            count2+=1
            dif2+=two-fist

    superioridade_media = dif/len(a)
    superioridade_porcent = (count*100)/len(a)
    return superioridade_porcent, superioridade_media


def variancia2(closes):
    v = 0
    mean = sum(closes)/len(closes)
    for close in closes:
        v += (close - mean)**2
    v /= len(closes)-1
    return v

def sdp2(closes):
    count=0
    for c in closes:
        if c<0:
            count+=c**2
    return (count/len(closes))**0.5

def sdp(closes, n=1, taxa_livre_risco=0):
    count = closes[0] - 1 if closes[0]>n else 0
    for c in range(1, len(closes)):
        value = closes[c] 
        if value - closes[c-1]<taxa_livre_risco:
            count += (value**2)
    return (count/len(closes))**0.5

# a = [10, 6, -12, 1, -8, -3, 8, 7, -9, -7]

# s = variancia(a)**0.5