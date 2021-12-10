
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras import regularizers
from keras.layers import LSTM
from tensorflow.keras.optimizers import SGD
import keras
from functions import *

TICKS = 20
N_INPUTS = 5
COLUMN_NAME = 'Rate Close'

def custom_loss_1(y_true, y_pred):
    def check_dirc(y_t, y_p):
        return True if y_t*y_p>0 else False
    penal = 0.20
    tensor = []
    for y_t, y_p  in zip(y_true[0], y_pred[0]):
        value = (y_t - y_p)
        if check_dirc(y_t, y_p):
            value += penal
        tensor.append(value)
    return tensor

dataset = pd.read_csv(r"history_datas\AAPL_1d.csv", sep='\t')

dataset = creat_rate_close(dataset, 'Close', COLUMN_NAME)

dataset.drop(columns=['Date'], inplace=True)
dataset.drop(columns=['Close'], inplace=True)

X, Y = fit_dados(dataset, dataset[COLUMN_NAME].values, TICKS)

sc = MinMaxScaler(feature_range = (0, 1))

Y = sc.fit_transform(np.reshape(np.array(Y), (len(Y),1)))

X_train, X_test, y_train, y_test = train_test_split(X, Y,  test_size=0.3, shuffle=False)

def model_LSTM():
  regressor = Sequential()

  regressor.add(LSTM(units = 33, activation='tanh',  return_sequences = True, input_shape = (TICKS, N_INPUTS)))

  
  regressor.add(LSTM(units = 33,return_sequences = True, kernel_regularizer = regularizers.l2 (0.0001)))
 
  
  regressor.add(LSTM(units = 33, return_sequences = True))
 

  regressor.add(LSTM(units = 33))
 

  regressor.add(Dense(1, activation='tanh'))

  opt = SGD(lr=0.01, momentum=0.9)

  regressor.compile(optimizer='rmsprop', loss=custom_loss_1)
  
  return regressor

def model_DMLP():
  model = Sequential()

  model.add(Dense(2, activation="tanh", input_shape=(TICKS, N_INPUTS)))
  model.add(Dense(10))
  model.add(Dense(10))
  model.add(Dense(1, activation="tanh"))

  model.compile(optimizer = "adam", loss='mean_absolute_error')
  
  return model

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=20)

model = model_LSTM()
print(model.summary())

history = model.fit(X_train, y_train, validation_data=(X_test, y_test),  batch_size=100, epochs=200, verbose=1, callbacks=[es])

predicted_stock_price = model.predict(X_test) 

predicted_stock_price
