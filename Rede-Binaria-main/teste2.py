import tensorflow as tf
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout, Input, Embedding, Bidirectional, LSTM
from tensorflow.keras import regularizers

EMBEDDING_DIM = 300
max_length = 120
batch_size = 512
vocab_size = 1000
units = 300

from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout, Input, Embedding, Bidirectional, LSTM
from tensorflow.keras import regularizers

input_text = tf.keras.Input(shape= (max_length), batch_size=batch_size)

embedding_layer = tf.keras.layers.Embedding(vocab_size, EMBEDDING_DIM, input_length =max_length, name="Embedding_Layer_1")
embedding_sequence = embedding_layer(input_text)

HQ = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(units,recurrent_dropout=0.5,kernel_regularizer=regularizers.l2(0.001),return_sequences=True,name='Bidirectional_1'))(embedding_sequence)
HQ = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(units,recurrent_dropout=0.5,kernel_regularizer=regularizers.l2(0.001),name='Bidirectional_2'))(HQ)

print (HQ)