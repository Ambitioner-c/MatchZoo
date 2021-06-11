# coding=utf-8
# @Author: cfl
# @Time: 2021/5/14 11:13
import math
import pandas as pd
import random


def read_tsv(path, filename):
    df = pd.read_csv(path + filename + '.tsv', sep='\t',
                     usecols=['QuestionID', 'Question', 'SentenceID', 'Sentence', 'Label'])

    return df


def sample(df):
    # 获取question_id集合
    all_set = set(df['QuestionID'])
    all_len = len(all_set)
    print('{:<15} {:>5}'.format('总数:', len(all_set)))

    # 抽样：验证集+测试集
    dev_tes_len = int(3 / 10 * all_len)
    dev_tes_set = set(random.sample(all_set, dev_tes_len))
    # print('{:<15} {:>5}'.format('验证集+测试集:', len(dev_tes_set)))

    # 抽样：训练集
    tra_set = all_set - dev_tes_set
    print('{:<15} {:>5}'.format('训练集:', len(tra_set)))

    # 抽样：验证集
    dev_len = int(1 / 3 * dev_tes_len)
    dev_set = set(random.sample(dev_tes_set, dev_len))
    print('{:<15} {:>5}'.format('验证集:', len(dev_set)))

    # 抽样：测试集
    tes_set = dev_tes_set - dev_set
    print('{:<15} {:>5}'.format('测试集:', len(tes_set)))

    tra = df[df['QuestionID'].isin(tra_set)]
    dev = df[df['QuestionID'].isin(dev_set)]
    tes = df[df['QuestionID'].isin(tes_set)]
    return tra, dev, tes


def write_tsc(tra, dev, tes, path, filename):
    tra.to_csv(path + 'train.tsv', sep='\t', index=False)
    print('File: train.tsv finished.')

    dev.to_csv(path + 'dev.tsv', sep='\t', index=False)
    print('File: dev.tsv finished.')

    tes.to_csv(path + 'test.tsv', sep='\t', index=False)
    print('File: test.tsv finished.')


if __name__ == '__main__':
    _path = '../Data/video_games_sort_copy/'
    _filename = 'video_games'

    # 读取全部tsv
    _df = read_tsv(_path, _filename)

    # 抽样
    _tra, _dev, _tes = sample(_df)

    write_tsc(_tra, _dev, _tes, _path, _filename)
