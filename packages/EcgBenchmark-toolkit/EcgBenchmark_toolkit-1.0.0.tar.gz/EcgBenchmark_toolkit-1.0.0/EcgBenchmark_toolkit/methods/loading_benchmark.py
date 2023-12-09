import os
import numpy as np
import pandas as pd


def fusion_benchmark():
    feature_extractors_merged = np.load('../benchmark/Features_fusion.npy')
    labels = np.load('../benchmark/Labels_fusion.npy')
    return feature_extractors_merged, labels


def binary_benchmark(abnormal_label):
    for file in os.listdir('../benchmark/' + abnormal_label + '+N/'):
        data = pd.read_csv('../benchmark/' + abnormal_label + '+N/' + file).dropna().drop_duplicates()
        features = data.iloc[:, :-1]
        labels = data.iloc[:, -1]
        return features, labels


def multiple_benchmark():
    data = pd.read_csv('../benchmark/Multi_Benchmark.csv').dropna().drop_duplicates()
    features = data.iloc[:, :-1]
    labels = data.iloc[:, -1]
    return features, labels


