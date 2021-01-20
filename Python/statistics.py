# coding=utf-8
# @Author: cfl
# @Time: 2021/1/20 9:30

import json
import pandas as pd


def parse(path):
    file = open(path, 'r')
    for j in file:
        yield json.dumps(eval(j))


def statistics(path):
    helpful_dict = dict()
    for j in parse(path):
        items = json.loads(j)
        questions = items['questions']
        for k in questions:
            answers = k['answers']
            total = 0
            for m in answers:
                total += m['helpful'][1]
            for m in answers:
                helpful = m['helpful'][0]
                if helpful >= total/2:
                    if str(helpful) not in helpful_dict:
                        helpful_dict[str(helpful)] = 1
                    else:
                        helpful_dict[str(helpful)] += 1

    return helpful_dict


if __name__ == '__main__':
    _path = '../Data/clothing_shoes_jewelry/QA_Clothing_Shoes_and_Jewelry.json'
    _helpful_dict = statistics(_path)
    print(_helpful_dict)
