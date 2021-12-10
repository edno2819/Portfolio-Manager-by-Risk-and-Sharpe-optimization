import numpy as np

def binario(valor):
    bi=[]
    for c in range(1,len(valor)):
        if valor[c]>valor[c-1]:
            bi.append(1)
        elif valor[c]<valor[c-1]:
            bi.append(0)
        elif valor[c]==valor[c-1]:
            bi.append(0.5)
    return bi

def filtro(real,predito):   
    d=[]
    g=0
    for c in range(0,len(predito)):
        if predito[c]==-1 or real[c]==-1:
            d.append(c-g)
            g+=1
    for c in range(0,len(d)):
        del(real[d[c]])
        del(predito[d[c]])
            
    return real,predito

def fit_dados(df:object, df_y:list, tick_treino:int):
    X_train = []
    y_train = []
    dados_ptreino = len(df)
    for i in range(tick_treino, dados_ptreino-1):
        temp = []
        for c in range(i-tick_treino,i):
            temp.append(df[c:c+1].values.tolist()[0])
        y_train.append(df_y[i])
        X_train.append(temp)

    X_train, y_train = np.array(X_train), np.array(y_train)
    
    return X_train,y_train

def creat_rate_close(dataset, column_name, COLUMN_NAME):
    rate_close = [0.001]
    for close in range(1, len(dataset[column_name])):
        rc = (dataset[column_name][close] - dataset[column_name][close-1])/dataset[column_name][close-1]
        rate_close.append(rc)
    dataset[COLUMN_NAME] = rate_close
    return dataset


