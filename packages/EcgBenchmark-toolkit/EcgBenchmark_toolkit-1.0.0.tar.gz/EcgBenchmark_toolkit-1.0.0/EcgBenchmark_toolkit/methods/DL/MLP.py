import tensorflow as tf


# 构建MLP模型
def build_MLP(types):
    new_model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(250,)),
        tf.keras.layers.Dense(10, activation='relu'),
        # tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(types, activation='softmax')
    ])
    return new_model
