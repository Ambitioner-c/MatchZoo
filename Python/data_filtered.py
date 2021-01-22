# coding=utf-8
# @Author: cfl
# @Time: 2020/12/30 15:16
import pandas
import csv


def read_csv(path):
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        result = list(reader)

    return result[1:]


def filtered(result):
    id_left = []
    text_left = []
    id_right = []
    text_right = []
    label = []
    
    new_id_left = []
    temporary = dict()

    for j in result:
        if j[1] not in temporary:
            temporary[j[1]] = float(j[5])
        else:
            temporary[j[1]] += float(j[5])

    for j in temporary:
        if temporary[j] > 0.0:
            new_id_left.append(j)
    
    for j in result:
        if j[1] in new_id_left:
            id_left.append(j[1])
            text_left.append(j[2])
            id_right.append(j[3])
            text_right.append(j[4])
            label.append(j[5])
    
    return id_left, text_left, id_right, text_right, label


def write_dev_csv(dev):
    dev.to_csv('../Data/clothing_shoes_jewelry/dev.csv')
    print('File: dev.csv finished.')


def write_test_csv(dev):
    dev.to_csv('../Data/clothing_shoes_jewelry/test.csv')
    print('File: dev.csv finished.')
    
    
if __name__ == '__main__':
    _path = '../Data/clothing_shoes_jewelry/dev_u.csv'
    _result = read_csv(_path)
    
    _id_left, _text_left, _id_right, _text_right, _label = filtered(_result)
    
    _dev = pandas.DataFrame({'id_left': _id_left,
                             'text_left': _text_left,
                             'id_right': _id_right,
                             'text_right': _text_right,
                             'label': _label})
    write_dev_csv(_dev)

    _path = '../Data/clothing_shoes_jewelry/test_u.csv'
    _result = read_csv(_path)

    _id_left, _text_left, _id_right, _text_right, _label = filtered(_result)

    _dev = pandas.DataFrame({'id_left': _id_left,
                             'text_left': _text_left,
                             'id_right': _id_right,
                             'text_right': _text_right,
                             'label': _label})
    write_test_csv(_dev)
