import tensorflow as tf


# 构建DNN模型
def build_DNN(types):
    # 创建一个Sequential模型
    new_model = tf.keras.Sequential()
    # 输入层
    new_model.add(tf.keras.layers.Input(shape=(250,)))
    # 添加隐藏层
    new_model.add(tf.keras.layers.Dense(128, activation='relu'))
    new_model.add(tf.keras.layers.Dense(64, activation='relu'))
    new_model.add(tf.keras.layers.Dense(32, activation='relu'))
    # 输出层
    new_model.add(tf.keras.layers.Dense(types, activation='softmax'))
    return new_model
