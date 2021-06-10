# coding=utf-8
# @Author: cfl
# @Time: 2021/5/14 17:21
import pandas as pd


def read_tsv(path):
    df = pd.read_csv(path, sep=' ')

    return df


def create_filtered(df):
    ref = []
    filtered = []

    question_id_set = dict()
    for index, row in df.iterrows():
        question_id = row[0]
        label = row[3]

        if question_id not in question_id_set:
            question_id_set[question_id] = label
        else:
            question_id_set[question_id] += label

    for j in question_id_set:
        if question_id_set[j] != 0:
            filtered.append(j)

    for index, row in df.iterrows():
        question_id = row[0]
        if question_id in filtered:
            ref.append([row[0], row[1], row[2], row[3]])

    return pd.DataFrame(ref)


def write_tsv(filtered, path, filename):
    filtered.to_csv(path + filename + '-filtered.ref', sep=' ', index=False, header=None)
    print('File: %s.ref finished.' % filename)


if __name__ == '__main__':
    _path = '../Data/video_games/'
    filename_list = ['dev', 'test']

    for i in filename_list:
        # 读取tsv文件
        _df = read_tsv(_path + i + '.ref')
        # print(_df)

        # 得到filtered格式
        _filtered = create_filtered(_df)

        # 写入
        write_tsv(_filtered, _path, i)
