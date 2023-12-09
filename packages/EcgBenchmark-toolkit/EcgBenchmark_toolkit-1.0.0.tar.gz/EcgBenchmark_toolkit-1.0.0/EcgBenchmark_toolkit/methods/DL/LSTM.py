import tensorflow as tf


def build_LSTM(types):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Input(shape=(250, 1)))
    model.add(tf.keras.layers.LSTM(200, return_sequences=True))
    model.add(tf.keras.layers.GlobalMaxPooling1D())
    model.add(tf.keras.layers.Dense(100, activation='relu'))
    model.add(tf.keras.layers.Dense(50, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(types, activation='softmax'))
    return model
