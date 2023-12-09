import numpy as np
import pandas as pd
from keras.callbacks import EarlyStopping
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import recall_score, precision_score, \
    f1_score, accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from Plotting import plot_heat_map
from DL.CNN import build_CNN
from DL.DNN import build_DNN
from DL.MLP import build_MLP
from EcgBenchmark_toolkit.methods.DL.LSTM import build_LSTM
# 随机种子
RANDOM_SEED = 42
BATCH_SIZE = 128
# 设置其他参数


def load_binary_data(df, RATIO):
    features = df.iloc[:, :-1]
    labels = df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=RATIO, random_state=RANDOM_SEED)
    return X_train, X_test, y_train, y_test


def machinelearning(df, types=2, test_size=0.3, epochs=20):
    # 定义模型列表
    models_ML = []
    # DecisionTree
    models_ML.append(DecisionTreeClassifier(max_depth=4))
    # RandomForest
    models_ML.append(RandomForestClassifier(n_estimators=100, random_state=90))
    # AdaBoost
    models_ML.append(AdaBoostClassifier())
    # SVM
    models_ML.append(SVC())
    # Beyes
    models_ML.append(GaussianNB())
    # KNN
    models_ML.append(KNeighborsClassifier(n_neighbors=2))
    # Logistic
    models_ML.append(LogisticRegression())
    # QuadraticDiscriminantAnalysis
    models_ML.append(QuadraticDiscriminantAnalysis())
    # # 深度学习模型
    models_DL = []
    models_DL.append(build_MLP(types))
    models_DL.append(build_DNN(types))
    models_DL.append(build_CNN(types))
    models_DL.append(build_LSTM(types))
    scores = []
    index = 0
    X_train, X_test, y_train, y_test = load_binary_data(df, test_size)
    for target_model in models_ML:
        print('continue')
        target_model.fit(X_train, y_train)
        y_pred = target_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred)
        scores.append([accuracy, precision, recall, f1, auc])
        plot_heat_map(y_test, y_pred, types)
        index += 1
    for model in models_DL:
        print('continue')
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        model.summary()
        # 创建一个 EarlyStopping 回调函数
        early_stopping = EarlyStopping(monitor='val_loss', patience=3, mode='min')
        # 指定训练的轮数(epochs)、批次大小(batch_size)和验证数据(validation_data))
        history = model.fit(X_train, y_train, epochs=epochs, batch_size=BATCH_SIZE,
                            validation_data=(X_test, y_test), callbacks=early_stopping)
        y_pred = np.argmax(model.predict(X_test), axis=-1)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred)
        scores.append([accuracy, precision, recall, f1, auc])
        plot_heat_map(y_test, y_pred, types)
        index += 1
    output = pd.DataFrame(data=scores, columns=['accuracy', 'precision', 'recall', 'f1', 'roc_auc'])
    print(output)

