# coding=utf-8
# @Author: cfl
# @Time: 2021/1/20 20:45
import pandas as pd
import csv


def _read_csv(path):
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        result = list(reader)

    return result[1:]


def _statistics(lines):
    question_id_dict = dict()
    question_label_set = set()
    for j in lines:
        question_id = j[1]
        label = j[5]
        if question_id not in question_id_dict:
            question_id_dict[question_id] = 1
        else:
            question_id_dict[question_id] += 1

        if label == '1.0':
            question_label_set.add(question_id)

    print("Num of question:")
    print("\t%d" % len(question_id_dict))

    answer_num_dict = dict()
    for j in question_id_dict:
        num = question_id_dict[j]
        if num not in answer_num_dict:
            answer_num_dict[num] = 1
        else:
            answer_num_dict[num] += 1

    print("Distribution of answers:")
    for j in sorted(answer_num_dict):
        print("\t%s\t%d" % (j, answer_num_dict[j]))

    answer_num_dict = dict()
    for j in question_label_set:
        num = question_id_dict[j]
        if num not in answer_num_dict:
            answer_num_dict[num] = 1
        else:
            answer_num_dict[num] += 1
    print("Distribution of answers where label is '1.0':")
    for j in sorted(answer_num_dict):
        print("\t%s\t%d" % (j, answer_num_dict[j]))


if __name__ == '__main__':
    _path = '../Data/clothing_shoes_jewelry/test.csv'
    _result = _read_csv(_path)

    _statistics(_result)
