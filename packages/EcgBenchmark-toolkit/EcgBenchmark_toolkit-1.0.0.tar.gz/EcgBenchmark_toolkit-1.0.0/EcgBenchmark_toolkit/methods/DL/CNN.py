import tensorflow as tf


# 构建CNN模型
def build_CNN(types):
    newModel = tf.keras.models.Sequential([
        tf.keras.layers.InputLayer(input_shape=(250, 1)),  # 输入大小为 (250, 1)
        tf.keras.layers.Conv1D(filters=3, kernel_size=3, strides=1, padding='SAME', activation='relu'),  # 卷积层
        tf.keras.layers.MaxPool1D(pool_size=2, strides=2, padding='SAME'),  # 最大池化层
        tf.keras.layers.Conv1D(filters=10, kernel_size=4, strides=1, padding='SAME', activation='relu'),  # 卷积层
        tf.keras.layers.MaxPool1D(pool_size=2, strides=2, padding='SAME'),  # 最大池化层
        tf.keras.layers.Conv1D(filters=20, kernel_size=4, strides=1, padding='SAME', activation='relu'),  # 卷积层
        tf.keras.layers.MaxPool1D(pool_size=2, strides=2, padding='SAME'),  # 最大池化层
        tf.keras.layers.Flatten(),  # 展平层
        tf.keras.layers.Dense(30, activation='relu'),  # 全连接层
        tf.keras.layers.Dense(20, activation='relu'),  # 全连接层
        tf.keras.layers.Dense(types, activation='softmax')  # 输出层
    ])
    return newModel
