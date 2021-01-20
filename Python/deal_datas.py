# coding=utf-8
# @Author: cfl
# @Time: 2020/12/23 17:14

import json
import pandas as pd


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

    left_num = 1
    for j in parse(path):
        items = json.loads(j)
        questions = items['questions']
        for k in questions:
            answers = k['answers']
            right_num = 0
            for m in answers:
                _question = ''
                _answers = []
                _question = str(k['questionText']).replace(',', ' ').\
                    replace('\ude03', '').replace('\ud83d', '').replace('\ude0a', '').\
                    replace('?', ' ').replace('\n', '').replace('\n\r', '')
                answer = str(m['answerText']).replace(',', ' ').\
                    replace('\ude03', '').replace('\ud83d', '').replace('\ude0a', '').\
                    replace('?', ' ').replace('\n', '').replace('\n\r', '')
                helpful = str(m['helpful'][0])
                if answer not in _answers and len(answer) < 500:
                    _answers.append(answer)

                for n in range(len(_answers)):
                    if helpful == '0':
                        id_left.append('Q' + str(left_num))
                        text_left.append(_question)
                        id_right.append('D'+str(left_num)+'-'+str(right_num))
                        text_right.append(_answers[n])
                        label.append(0.0)
                    else:
                        id_left.append('Q' + str(left_num))
                        text_left.append(_question)
                        id_right.append('D' + str(left_num) + '-' + str(right_num))
                        text_right.append(_answers[n])
                        label.append(1.0)
                right_num += 1
            left_num += 1

    return id_left, text_left, id_right, text_right, label


def write_csv(train, dev, test):
    train.to_csv('../Data/electronics/train.csv')
    print('File: train.csv finished.')

    dev.to_csv('../Data/electronics/dev_u.csv')
    print('File: dev.csv finished.')

    test.to_csv('../Data/electronics/test_u.csv')
    print('File: test.csv finished.')


if __name__ == '__main__':
    _path = '../Data/electronics/QA_Electronics.json'
    _id_left, _text_left, _id_right, _text_right, _label = recombination(_path)
    _length = len(_label)
    _df_train = pd.DataFrame({'id_left': _id_left[:int(0.5 * _length)],
                              'text_left': _text_left[:int(0.5 * _length)],
                              'id_right': _id_right[:int(0.5 * _length)],
                              'text_right': _text_right[:int(0.5 * _length)],
                              'label': _label[:int(0.5 * _length)]})

    _df_dev = pd.DataFrame({'id_left': _id_left[int(0.5 * _length):int(0.75 * _length)],
                            'text_left': _text_left[int(0.5 * _length):int(0.75 * _length)],
                            'id_right': _id_right[int(0.5 * _length):int(0.75 * _length)],
                            'text_right': _text_right[int(0.5 * _length):int(0.75 * _length)],
                            'label': _label[int(0.5 * _length):int(0.75 * _length)]})

    _df_test = pd.DataFrame({'id_left': _id_left[int(0.75 * _length):],
                             'text_left': _text_left[int(0.75 * _length):],
                             'id_right': _id_right[int(0.75 * _length):],
                             'text_right': _text_right[int(0.75 * _length):],
                             'label': _label[int(0.75 * _length):]})
    # _df_train = pd.DataFrame({'id_left': _id_left[540:590],
    #                           'text_left': _text_left[540:590],
    #                           'id_right': _id_right[540:590],
    #                           'text_right': _text_right[540:590],
    #                           'label': _label[540:590]})
    #
    # _df_dev = pd.DataFrame({'id_left': _id_left[590:610],
    #                         'text_left': _text_left[590:610],
    #                         'id_right': _id_right[590:610],
    #                         'text_right': _text_right[590:610],
    #                         'label': _label[590:610]})
    #
    # _df_test = pd.DataFrame({'id_left': _id_left[610:630],
    #                          'text_left': _text_left[610:630],
    #                          'id_right': _id_right[610:630],
    #                          'text_right': _text_right[610:630],
    #                          'label': _label[610:630]})
    # a = _id_left[:300]
    # a.extend(_id_left[:300])
    # b = _text_left[:300]
    # b.extend(_text_left[:300])
    # c = _id_right[:300]
    # c.extend(_id_right[:300])
    # d = _text_right[:300]
    # d.extend(_text_right[:300])
    # e = _label[:300]
    # e.extend(_label[:300])
    # _df_train = pd.DataFrame({'id_left': a,
    #                           'text_left': b,
    #                           'id_right': c,
    #                           'text_right': d,
    #                           'label': e})
    # a = _id_left[300:420]
    # a.extend(_id_left[300:420])
    # b = _text_left[300:420]
    # b.extend(_text_left[300:420])
    # c = _id_right[300:420]
    # c.extend(_id_right[300:420])
    # d = _text_right[300:420]
    # d.extend(_text_right[300:420])
    # e = _label[300:420]
    # e.extend(_label[300:420])
    # _df_dev = pd.DataFrame({'id_left': a,
    #                         'text_left': b,
    #                         'id_right': c,
    #                         'text_right': d,
    #                         'label': e})
    # a = _id_left[420:630]
    # a.extend(_id_left[420:630])
    # b = _text_left[420:630]
    # b.extend(_text_left[420:630])
    # c = _id_right[420:630]
    # c.extend(_id_right[420:630])
    # d = _text_right[420:630]
    # d.extend(_text_right[420:630])
    # e = _label[420:630]
    # e.extend(_label[420:630])
    # _df_test = pd.DataFrame({'id_left': a,
    #                          'text_left': b,
    #                          'id_right': c,
    #                          'text_right': d,
    #                          'label': e})
    write_csv(_df_train, _df_dev, _df_test)


# # coding=utf-8
# # @Author: cfl
# # @Time: 2020/12/23 17:14
#
# import json
# import pandas as pd
#
#
# def parse(path):
#     file = open(path, 'r')
#     for j in file:
#         yield json.dumps(eval(j))
#
#
# def recombination(path):
#     id_left = []
#     text_left = []
#     id_right = []
#     text_right = []
#     label = []
#
#     left_num = 1
#     for j in parse(path):
#         for copy in range(2):
#             items = json.loads(j)
#             questions = items['questions']
#             for k in questions:
#                 answers = k['answers']
#                 right_num = 0
#                 for m in answers:
#                     _question = ''
#                     _answers = []
#                     _question = str(k['questionText']).replace(',', ' ').\
#                         replace('\ude03', '').replace('\ud83d', '').replace('\ude0a', '').\
#                         replace('?', ' ').replace('\n', '').replace('\n\r', '')
#                     answer = str(m['answerText']).replace(',', ' ').\
#                         replace('\ude03', '').replace('\ud83d', '').replace('\ude0a', '').\
#                         replace('?', ' ').replace('\n', '').replace('\n\r', '')
#                     helpful = str(m['helpful'][0])
#                     if answer not in _answers:
#                         _answers.append(answer)
#
#                     for n in range(len(_answers)):
#                         if helpful == '0':
#                             id_left.append('Q' + str(left_num))
#                             text_left.append(_question)
#                             id_right.append('D'+str(left_num)+'-'+str(right_num))
#                             text_right.append(_answers[n])
#                             label.append(0.0)
#                         else:
#                             id_left.append('Q' + str(left_num))
#                             text_left.append(_question)
#                             id_right.append('D' + str(left_num) + '-' + str(right_num))
#                             text_right.append(_answers[n])
#                             label.append(1.0)
#                     right_num += 1
#                 left_num += 1
#
#     return id_left, text_left, id_right, text_right, label
#
#
# def write_csv(train, dev, test):
#     train.to_csv('../Data/clothing_shoes_jewelry/train.csv')
#     print('File: train.csv finished.')
#
#     dev.to_csv('../Data/clothing_shoes_jewelry/dev_u.csv')
#     print('File: dev.csv finished.')
#
#     test.to_csv('../Data/clothing_shoes_jewelry/test_u.csv')
#     print('File: test.csv finished.')
#
#
# if __name__ == '__main__':
#     _path = '../Data/clothing_shoes_jewelry/QA_Clothing_Shoes_and_Jewelry.json'
#     _id_left, _text_left, _id_right, _text_right, _label = recombination(_path)
#     _length = len(_label)
#     # _df_train = pd.DataFrame({'id_left': _id_left[:int(0.5 * _length)],
#     #                           'text_left': _text_left[:int(0.5 * _length)],
#     #                           'id_right': _id_right[:int(0.5 * _length)],
#     #                           'text_right': _text_right[:int(0.5 * _length)],
#     #                           'label': _label[:int(0.5 * _length)]})
#     #
#     # _df_dev = pd.DataFrame({'id_left': _id_left[int(0.5 * _length):int(0.75 * _length)],
#     #                         'text_left': _text_left[int(0.5 * _length):int(0.75 * _length)],
#     #                         'id_right': _id_right[int(0.5 * _length):int(0.75 * _length)],
#     #                         'text_right': _text_right[int(0.5 * _length):int(0.75 * _length)],
#     #                         'label': _label[int(0.5 * _length):int(0.75 * _length)]})
#     #
#     # _df_test = pd.DataFrame({'id_left': _id_left[int(0.75 * _length):],
#     #                          'text_left': _text_left[int(0.75 * _length):],
#     #                          'id_right': _id_right[int(0.75 * _length):],
#     #                          'text_right': _text_right[int(0.75 * _length):],
#     #                          'label': _label[int(0.75 * _length):]})
#     _df_train = pd.DataFrame({'id_left': _id_left[:600],
#                               'text_left': _text_left[:600],
#                               'id_right': _id_right[:600],
#                               'text_right': _text_right[:600],
#                               'label': _label[:600]})
#
#     _df_dev = pd.DataFrame({'id_left': _id_left[600:840],
#                             'text_left': _text_left[600:840],
#                             'id_right': _id_right[600:840],
#                             'text_right': _text_right[600:840],
#                             'label': _label[600:840]})
#
#     _df_test = pd.DataFrame({'id_left': _id_left[840:1080],
#                              'text_left': _text_left[840:1080],
#                              'id_right': _id_right[840:1080],
#                              'text_right': _text_right[840:1080],
#                              'label': _label[840:1080]})
#     # a = _id_left[:300]
#     # a.extend(_id_left[:300])
#     # b = _text_left[:300]
#     # b.extend(_text_left[:300])
#     # c = _id_right[:300]
#     # c.extend(_id_right[:300])
#     # d = _text_right[:300]
#     # d.extend(_text_right[:300])
#     # e = _label[:300]
#     # e.extend(_label[:300])
#     # _df_train = pd.DataFrame({'id_left': a,
#     #                           'text_left': b,
#     #                           'id_right': c,
#     #                           'text_right': d,
#     #                           'label': e})
#     # a = _id_left[300:420]
#     # a.extend(_id_left[300:420])
#     # b = _text_left[300:420]
#     # b.extend(_text_left[300:420])
#     # c = _id_right[300:420]
#     # c.extend(_id_right[300:420])
#     # d = _text_right[300:420]
#     # d.extend(_text_right[300:420])
#     # e = _label[300:420]
#     # e.extend(_label[300:420])
#     # _df_dev = pd.DataFrame({'id_left': a,
#     #                         'text_left': b,
#     #                         'id_right': c,
#     #                         'text_right': d,
#     #                         'label': e})
#     # a = _id_left[420:630]
#     # a.extend(_id_left[420:630])
#     # b = _text_left[420:630]
#     # b.extend(_text_left[420:630])
#     # c = _id_right[420:630]
#     # c.extend(_id_right[420:630])
#     # d = _text_right[420:630]
#     # d.extend(_text_right[420:630])
#     # e = _label[420:630]
#     # e.extend(_label[420:630])
#     # _df_test = pd.DataFrame({'id_left': a,
#     #                          'text_left': b,
#     #                          'id_right': c,
#     #                          'text_right': d,
#     #                          'label': e})
#     write_csv(_df_train, _df_dev, _df_test)
