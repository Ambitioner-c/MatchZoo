# coding=utf-8
# @Author: cfl
# @Time: 2020/12/23 17:14

import json
import pandas as pd
import numpy as np
import time


def parse(path):
    file = open(path, 'r')
    for j in file:
        yield json.dumps(eval(j))


def time_stamp(answer_time):
    month = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
             'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}
    answer_time_list = answer_time.replace(',', '').split(' ')
    answer_time_format = month[answer_time_list[0]] + '-' + answer_time_list[1] + '-' + answer_time_list[2]
    answer_time_struct = time.strptime(answer_time_format, '%m-%d-%Y')
    timestamp = time.mktime(answer_time_struct)

    return timestamp


def recombination(path):
    id_left = []
    text_left = []
    id_right = []
    text_right = []
    label = []
    timestamp = []

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
                    replace('\n', '').replace('\n\r', '').replace('\\x', '')
                helpful = m['helpful'][0]

                # 时间戳
                timestamp.append(time_stamp(str(m['answerTime'])))

                if len(_question) > 512:
                    _question = _question[:512]
                if len(answer) > 512:
                    answer = answer[:512]

                # 有人认为有用即为有用
                if helpful is not 0:
                    id_left.append('Q' + str(left_num))
                    text_left.append(_question)
                    id_right.append('D' + str(left_num) + '-' + str(right_num))
                    text_right.append(answer)
                    # label.append(1)

                    # 为后续排序做铺垫
                    label.append(helpful)
                else:
                    id_left.append('Q' + str(left_num))
                    text_left.append(_question)
                    id_right.append('D'+str(left_num)+'-'+str(right_num))
                    text_right.append(answer)
                    # label.append(0)

                    # 为后续排序做铺垫
                    label.append(helpful)
                right_num += 1
            left_num += 1

    return id_left, text_left, id_right, text_right, label, timestamp


def sort(df, length):
    # df = df.sort_values('Timestamp', ascending=False)
    # print(df)
    #
    # groups = df.sort_values('Label', ascending=False).groupby('QuestionID')
    # print(groups)
    #
    # n = 0
    # for _, group in groups:
    #     print(_)
    #     print(group)
    #     print(type(group))
    #     if n == 10:
    #         break
    #     n += 1
    groups = df.sort_values('Timestamp', ascending=False).groupby('QuestionID')

    # singles = []
    group_dict = dict()
    # n = 0
    for _, group in groups:
        # print(_)
        # print(group)

        group_dict[_] = group
        # singles.append(group)
        # if n == 10:
        #     break
        # n += 1
    # new_df = pd.concat(singles, ignore_index=True)
    # print(new_df)

    # print(group_dict)

    singles = []
    for j in range(length):
        question_id = 'Q' + str(j)
        singles.append(group_dict[question_id])
    new_df = pd.concat(singles, ignore_index=True)
    # print(new_df)

    return new_df


def write_tsc(df, path, filename):
    df.to_csv(path + filename + '.tsv', sep='\t', index=False)
    print('File: video_games_sort.tsv finished.')

    # train, validate, test = np.split(df.sample(frac=1), [int(.7*len(df)), int(.8*len(df))])


if __name__ == '__main__':
    _path = '../Data/video_games_sort_copy/'
    _filename = 'video_games'
    _id_left, _text_left, _id_right, _text_right, _label, _timestamp = recombination(_path + _filename + '.json')
    _length = len(set(_id_left))
    # 构造完整的tsv
    _df = pd.DataFrame({'QuestionID': _id_left,
                        'Question': _text_left,
                        'SentenceID': _id_right,
                        'Sentence': _text_right,
                        'Label': _label,
                        'Timestamp': _timestamp})

    # 排序
    _new_df = sort(_df, _length)

    # 写入完整tsv
    write_tsc(_new_df, _path, _filename)
