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
