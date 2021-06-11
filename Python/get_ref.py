# coding=utf-8
# @Author: cfl
# @Time: 2021/5/14 16:34
import pandas as pd


def read_tsv(path):
    df = pd.read_csv(path, sep='\t')

    return df


def create_ref(df):
    num_1 = 0
    ref = []

    question_id_set = set()
    for index, row in df.iterrows():
        question_id = row['QuestionID']
        sentence_id = row['SentenceID']
        label = row['Label']
        if int(label) > 0:
            label = 1
        else:
            label = 0

        if question_id not in question_id_set:
            num_1 += 1
            question_id_set.add(question_id)

            num_2 = int(sentence_id.split('-')[1])

            ref.append([num_1, 0, num_2, int(label)])
        else:
            num_2 = int(sentence_id.split('-')[1])

            ref.append([num_1, 0, num_2, int(label)])

    return pd.DataFrame(ref)


def write_tsv(ref, path, filename):
    ref.to_csv(path + filename + '.ref', sep=' ', index=False, header=None)
    print('File: %s.ref finished.' % filename)


if __name__ == '__main__':
    _path = '../Data/video_games_sort_copy/'
    filename_list = ['train', 'dev', 'test']

    for i in filename_list:
        # 读取tsv文件
        _df = read_tsv(_path + i + '.tsv')
        # print(_df)

        # 得到ref格式
        _ref = create_ref(_df)

        # 写入
        write_tsv(_ref, _path, i)


