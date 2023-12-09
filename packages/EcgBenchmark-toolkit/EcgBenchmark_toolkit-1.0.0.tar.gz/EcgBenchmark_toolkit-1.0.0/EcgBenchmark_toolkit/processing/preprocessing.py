import os
from collections import Counter
import numpy as np
import pywt
import wfdb
from scipy import signal
set_abnormal_type_ratio = 0.7


def denoise(data):
    # 使用小波变换对信号进行分解
    coeffs = pywt.wavedec(data=data, wavelet='db5', level=9)
    cA9, cD9, cD8, cD7, cD6, cD5, cD4, cD3, cD2, cD1 = coeffs
    # 使用软阈值对分解后的系数进行去噪
    threshold = (np.median(np.abs(cD1)) / 0.6745) * (np.sqrt(2 * np.log(len(cD1))))
    cD1.fill(0)
    cD2.fill(0)
    for i in range(1, len(coeffs) - 2):
        coeffs[i] = pywt.threshold(coeffs[i], threshold)
    # 通过逆小波变换得到去噪后的信号
    rdata = pywt.waverec(coeffs=coeffs, wavelet='db5')
    return rdata


def binary_processing(path, frequency, abnormal_label, label_location='symbol'):
    Seqs = []
    Labels = []
    try:
        for file in os.listdir(path):
            name = os.path.splitext(file)[0]
            print(name)
            try:
                annotation = wfdb.rdann(path + '/' + name, 'atr')
                samples = annotation.sample
                if label_location == 'symbol':
                    symbols = annotation.symbol
                else:
                    symbols = [s.lstrip('(').replace('\x00', '') for s in annotation.aux_note]
                # 筛去N类型，统计异常类型及总数
                filtered_symbol = [s for s in symbols if s != 'N']
                abnormal_types = Counter(filtered_symbol)
                total_abnormal_types = sum(abnormal_types.values())
                # 无异常，则筛取(有待改进)
                if total_abnormal_types == 0:
                    continue
                # 计算最高异常占总异常的比例
                max_abnormal_type_count = max(abnormal_types.values())
                max_abnormal_type_ratio = max_abnormal_type_count / total_abnormal_types
                # 判断占比是否达标
                if max_abnormal_type_ratio <= set_abnormal_type_ratio:
                    continue
                record = wfdb.rdrecord(path + '/' + name, channels=[0])
                rdata = record.p_signal.flatten()
                rdata = denoise(data=rdata)
                i = 0
                j = len(annotation.symbol) - 1
                while i < j:
                    i += 1
                    try:
                        if samples[i] - frequency / 2 <= 0:
                            continue
                        elif samples[i] + frequency / 2 > len(rdata):
                            break
                        if symbols[i] == abnormal_label or symbols[i] == 'N':
                            seq_origin = rdata[samples[i] - int(frequency / 2):samples[i] + int(frequency / 2)]
                            seq_resampled = signal.resample(seq_origin, 250)
                            if symbols[i] == abnormal_label:
                                seq_resampled = np.append(seq_resampled, [1])
                                Labels.append(1)
                            else:
                                seq_resampled = np.append(seq_resampled, [0])
                                Labels.append(0)
                            Seqs.append(seq_resampled)
                    except ValueError:
                        return 0
            except ValueError:
                return 0
    except Exception:
        return 0
    abnormal_types = Counter(Labels)
    print(abnormal_types.keys(), abnormal_types.values())
    return Seqs


def multiple_processing(path, frequency, Abnormal_Labels, label_location='symbol'):
    Seqs = []
    Labels = []
    try:
        for file in os.listdir(path):
            name = os.path.splitext(file)[0]
            print(name)
            try:
                annotation = wfdb.rdann(path + '/' + name, 'atr')
                samples = annotation.sample
                if label_location == 'symbol':
                    symbols = annotation.symbol
                else:
                    symbols = [s.lstrip('(').replace('\x00', '') for s in annotation.aux_note]
                # 筛去N类型，统计异常类型及总数
                filtered_symbol = [s for s in symbols if s != 'N']
                abnormal_types = Counter(filtered_symbol)
                total_abnormal_types = sum(abnormal_types.values())
                # 无异常，则筛取(有待改进)
                if total_abnormal_types == 0:
                    continue
                # 计算最高异常占总异常的比例
                max_abnormal_type_count = max(abnormal_types.values())
                max_abnormal_type_ratio = max_abnormal_type_count / total_abnormal_types
                # 判断占比是否达标
                if max_abnormal_type_ratio <= set_abnormal_type_ratio:
                    continue
                record = wfdb.rdrecord(path + '/' + name, channels=[0])
                rdata = record.p_signal.flatten()
                rdata = denoise(data=rdata)
                i = 0
                j = len(annotation.symbol) - 1
                while i < j:
                    i += 1
                    try:
                        if samples[i] - frequency / 2 <= 0:
                            continue
                        elif samples[i] + frequency / 2 > len(rdata):
                            break
                        if symbols[i] in Abnormal_Labels:
                            label = np.where(Abnormal_Labels == symbols[i])[0][0]
                            seq_origin = rdata[samples[i] - int(frequency / 2):samples[i] + int(frequency / 2)]
                            seq_resampled = signal.resample(seq_origin, 250)
                            seq_resampled = np.append(seq_resampled, [label])
                            Labels.append(label)
                            Seqs.append(seq_resampled)
                    except ValueError:
                        return 0
            except ValueError:
                return 0
    except Exception:
        return 0
    abnormal_types = Counter(Labels)
    print(abnormal_types.keys(), abnormal_types.values())
    return Seqs
