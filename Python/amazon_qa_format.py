# coding=utf-8
# @Author: cfl
# @Time: 2020/12/23 17:14

import json
import pandas as pd
import numpy as np


def parse(path):
    file = open(path, 'r')
    for j in file:
        yield json.dumps(eval(j))


def recombination(path):
    id_left = []
    text_left = []
    id_right = []
    text_right = []
    label = []

    left_num = 0
    for j in parse(path):
        items = json.loads(j)
        questions = items['questions']
        for k in questions:
            answers = k['answers']
            right_num = 0

            for m in answers:
                _question = ''
                _question = str(k['questionText']).replace('\t', ' ').\
                    replace('\ude03', '').replace('\ud83d', '').replace('\ude0a', '').\
                    replace('\n', '').replace('\n\r', '')
                answer = str(m['answerText']).replace('\t', ' ').\
                    replace('\ude03', '').replace('\ud83d', '').replace('\ude0a', '').\
                    replace('\n', '').replace('\n\r', '')
                helpful = m['helpful'][0]

                if len(answer) > 512:
                    answer = answer[:512]

                # 有人认为有用即为有用
                if helpful is not 0:
                    id_left.append('Q' + str(left_num))
                    text_left.append(_question)
                    id_right.append('D' + str(left_num) + '-' + str(right_num))
                    text_right.append(answer)
                    label.append(1)
                else:
                    id_left.append('Q' + str(left_num))
                    text_left.append(_question)
                    id_right.append('D'+str(left_num)+'-'+str(right_num))
                    text_right.append(answer)
                    label.append(0)
                right_num += 1
            left_num += 1

    return id_left, text_left, id_right, text_right, label


def write_tsc(df, path, filename):
    df.to_csv(path + filename + '.tsv', sep='\t', index=False)
    print('File: video_games.tsv finished.')

    # train, validate, test = np.split(df.sample(frac=1), [int(.7*len(df)), int(.8*len(df))])


if __name__ == '__main__':
    _path = '../Data/video_games/'
    _filename = 'video_games'
    _id_left, _text_left, _id_right, _text_right, _label = recombination(_path + _filename + '.json')
    _length = len(_label)
    # 构造完整的tsv
    _df = pd.DataFrame({'QuestionID': _id_left,
                        'Question': _text_left,
                        'SentenceID': _id_right,
                        'Sentence': _text_right,
                        'Label': _label})

    # 写入完整tsv
    write_tsc(_df, _path, _filename)
