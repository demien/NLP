# encoding=utf-8
import operator
import os
import pickle
import copy
import json
import sys
from collections import defaultdict
from constants import SEPRATOR, RETRIVE_COLUMNS, DATA_BASE_PATH, FORMATTED_OUTPUT_FILE, PICKLE_TOTAL_CUT_RESULT, \
    PICKLE_TOTAL_WORD_RESULT, PICKLE_TOTAL_CATEGORY_CNT
from tools import generate_defaultdict, print_result, format_keys
import jieba.posseg as pseg


CATEGORY = 2


def learning(input_path=FORMATTED_OUTPUT_FILE, category=1):
    if os.path.isfile(PICKLE_TOTAL_CUT_RESULT) and os.path.isfile(PICKLE_TOTAL_WORD_RESULT) and \
        os.path.isfile(PICKLE_TOTAL_CATEGORY_CNT):
        return pickle_load(PICKLE_TOTAL_CUT_RESULT), pickle_load(PICKLE_TOTAL_WORD_RESULT), \
            pickle_load(PICKLE_TOTAL_CATEGORY_CNT)
    total_word_result = defaultdict(int)
    total_cut_result = generate_defaultdict(category + 1, int)
    total_category_cnt = generate_defaultdict(category, int)
    cnt = 0
    with open(input_path, 'r') as input_file:
        for line in input_file:
            if cnt % 100 == 0:
                print cnt
            cnt += 1
            category_one, category_two, category_three, category_four, content, cid = line.split(SEPRATOR)
            line_cut_result = cut(line)
            categorys = [category_one, category_two, category_three, category_four][:category]
            categorys = format_keys(categorys)

            # total_word_result
            total_word_result = merge_word_count(total_word_result, line_cut_result)

            # total_cut_result
            total_cut_result_tmp = merge_word_count(get_deep_dict_value(total_cut_result, categorys), cut(line))
            set_deep_dict_value(total_cut_result, categorys, total_cut_result_tmp)

            # total_category_cnt
            total_category_cnt_tmp = get_deep_dict_value(total_category_cnt, categorys)
            set_deep_dict_value(total_category_cnt, categorys, total_category_cnt_tmp+1)

    pickle_dump(total_cut_result, PICKLE_TOTAL_CUT_RESULT)
    pickle_dump(total_word_result, PICKLE_TOTAL_WORD_RESULT)
    pickle_dump(total_category_cnt, PICKLE_TOTAL_CATEGORY_CNT)
    return total_cut_result, total_word_result, total_category_cnt


def cut(line):
    stop_words = [u'\u8ddf\u8fdb', u'\u529e\u7406', u'\u89e3\u91ca', u'\u8bf7', u'\u8c22\u8c22', u'\u65e0\u6cd5', u'\u610f\u89c1', u'\u53cd\u6620', u'\u63a5\u53d7', u'\u5305', u'\u6709', u'\u6237', u'\u95ee\u9898', u'\u5185\u5bb9', u'\u6838\u5b9e', u'\u4e0d\u5230', u'\u663e\u793a', u'\u4f7f\u7528', u'\u662f', u'\u7ed9\u4e88', u'\u8bf7', u'\u65e0\u6cd5', u'\u8c22\u8c22', u'\u89e3\u91ca', u'\u663e\u793a', u'\u95ee\u9898', u'\u63a5\u53d7', u'\u53cd\u6620', u'\u8ddf\u8fdb', u'\u5185\u5bb9', u'\u662f', u'\u8868\u793a', u'\u4f7f\u7528', u'\u4e89\u8bae', u'\u79f0', u'\u6211\u53f8', u'\u529e\u7406', u'\u6838\u5b9e', u'\u65f6', u'\u6ca1\u6709', u'\u76f8\u5173', u'\u5305', u'\u529e\u7406', u'\u4e89\u8bae', u'\u8bf7', u'\u89e3\u91ca', u'\u8c22\u8c22', u'\u53cd\u6620', u'\u6ca1\u6709', u'\u8ddf\u8fdb', u'\u6709', u'\u8868\u793a', u'\u65e0\u6545', u'\u63a5\u53d7', u'\u662f', u'\u6211\u53f8', u'\u5185\u5bb9', u'\u6838\u5b9e', u'\u56de\u590d', u'\u7ecf', u'\u8bf7', u'\u4e89\u8bae', u'\u89e3\u91ca', u'\u8c22\u8c22', u'\u663e\u793a', u'\u529e\u7406', u'\u53cd\u6620', u'\u8ddf\u8fdb', u'\u4f7f\u7528', u'\u63a5\u53d7', u'\u662f', u'\u5185\u5bb9', u'\u8868\u793a', u'\u6709', u'\u6211\u53f8', u'\u65e0\u6cd5', u'\u6ca1\u6709', u'\u95ee\u9898', u'\u5230', u'\u81f4\u7535', u'\u5305', u'\u76f8\u5173', u'\u56de\u590d', u'\u6237', u'\u5efa\u8bae', u'\u6838\u5b9e', u'\u8bf7', u'\u65e0\u6cd5', u'\u5305', u'\u8c22\u8c22', u'\u8868\u793a', u'\u53cd\u6620', u'\u662f', u'\u6ca1\u6709', u'\u6838\u5b9e', u'\u529e\u7406', u'\u9700\u8981', u'\u6709', u'\u514d', u'\u89e3\u91ca', u'\u79f0', u'\u7ecf', u'\u5206', u'\u90e8\u95e8', u'\u8fdb\u53bb', u'\u8ddf\u8fdb', u'\u5230', u'\u67e5', u'\u65e0\u6cd5', u'\u529e\u7406', u'\u8bf7', u'\u64cd\u4f5c', u'\u53cd\u6620', u'\u4e2d\u5fc3', u'\u7ed3\u679c', u'\u53cd\u9988', u'\u8d35\u90e8', u'\u7f51\u4e0a', u'\u8c22\u8c22', u'\u8bd5', u'\u5fd9', u'\u539f\u56e0', u'\u8bf7', u'\u5230', u'\u8c22\u8c22', u'\u6ca1\u6709', u'\u53cd\u6620', u'\u6838\u5b9e', u'\u65e0\u6cd5', u'\u89e3\u91ca', u'\u8868\u793a', u'\u6211\u53f8', u'\u63a5\u53d7', u'\u8ddf\u8fdb', u'\u6709', u'\u6536\u5230', u'\u95ee\u9898', u'\u624d\u4f1a\u8d62', u'\u7231\u5145', u'\u662f', u'\u56de\u590d', u'\u8d62', u'\u7ecf', u'\u53cd\u6620', u'\u5230', u'\u4e2d\u5fc3', u'\u6211\u53f8', u'\u662f', u'\u4e0d\u5230', u'\u529e\u7406', u'\u67e5', u'\u663e\u793a', u'\u65f6\u95f4', u'\u67e5\u4e0d\u5230', u'\u6237', u'\u7f16\u53f7', u'\u7f51\u4e0a', u'\u7248', u'\u65e0\u6cd5', u'\u89e3\u91ca', u'\u8bf7', u'\u8c22\u8c22', u'\u529e\u7406', u'\u5185\u5bb9', u'\u663e\u793a', u'\u63a5\u53d7', u'\u662f', u'\u53cd\u6620', u'\u4f7f\u7528', u'\u95ee\u9898', u'\u6211\u53f8', u'\u8868\u793a', u'\u6237', u'\u8ddf\u8fdb', u'\u5230', u'\u7f51\u4e0a', u'\u6709', u'\u6ca1\u6709', u'\u5efa\u8bae', u'\u6838\u5b9e', u'\u8bf7', u'\u6536\u5230', u'\u8c22\u8c22', u'\u6ca1\u6709', u'\u53cd\u6620', u'\u5185\u5bb9', u'\u6052\u5927', u'\u95ee\u9898', u'\u6211\u53f8', u'\u624d\u4f1a\u8d62', u'\u7231\u5145', u'\u5230', u'\u8d62', u'\u56de\u590d', u'\u4e89\u8bae', u'\u5efa\u8bae', u'\u79f0', u'\u4f1a', u'\u89e3\u91ca', u'\u8868\u793a', u'\u8ddf\u8fdb', u'\u65f6\u95f4', u'\u76f8\u5173', u'\u7ecf', u'\u53c2\u52a0', u'\u4e89\u8bae', u'\u89e3\u91ca', u'\u8bf7', u'\u8c22\u8c22', u'\u63a5\u53d7', u'\u8868\u793a', u'\u6709', u'\u6ca1\u6709', u'\u4f7f\u7528', u'\u8ddf\u8fdb', u'\u53cd\u6620', u'\u95ee\u9898', u'\u6838\u5b9e', u'\u6237', u'\u5230', u'\u5185\u5bb9', u'\u663e\u793a', u'\u662f', u'\u610f\u89c1', u'\u81f4\u7535', u'\u5efa\u8bae', u'\u9700\u8981', u'\u4ea7\u751f', u'\u6211\u53f8', u'\u5230', u'\u8bf7', u'\u8c22\u8c22', u'\u6ca1\u6709', u'\u89e3\u91ca', u'\u53cd\u6620', u'\u65e0\u6cd5', u'\u4e0d\u5230', u'\u6211\u53f8', u'\u6709', u'\u63a5\u53d7', u'\u8868\u793a', u'\u662f', u'\u6838\u5b9e', u'\u8ddf\u8fdb', u'\u5185\u5bb9', u'\u76f8\u5173', u'\u7ecf', u'\u79f0', u'\u663e\u793a', u'\u4f7f\u7528', u'\u8fdb\u884c', u'\u56de\u590d', u'\u81f4\u7535', u'\u65e0\u6cd5', u'\u662f', u'\u63a5\u53d7', u'\u89e3\u91ca', u'\u6237', u'\u539f\u56e0', u'\u4e2d\u5fc3', u'\u6e05\u7a7a', u'\u7ed9\u4e88', u'\u5efa\u8bae', u'\u8c22\u8c22', u'\u95ee\u9898', u'\u5355', u'\u529e\u7406', u'\u544a\u77e5', u'\u90e8', u'\u79f0', u'\u5185\u5bb9', u'\u8bf7', u'\u8ddf\u8fdb', u'\u5305', u'\u4e89\u8bae', u'\u529e\u7406', u'\u8bf7', u'\u89e3\u91ca', u'\u8c22\u8c22', u'\u53cd\u6620', u'\u6ca1\u6709', u'\u6709', u'\u8ddf\u8fdb', u'\u8868\u793a', u'\u63a5\u53d7', u'\u6211\u53f8', u'\u65e0\u6545', u'\u5185\u5bb9', u'\u6838\u5b9e', u'\u662f', u'\u5230', u'\u56de\u590d', u'\u7ecf', u'\u8bf7', u'\u8c22\u8c22', u'\u6ca1\u6709', u'\u9519', u'\u529e\u7406', u'\u53cd\u6620', u'\u6709', u'\u8868\u793a', u'\u89e3\u91ca', u'\u5230', u'\u662f', u'\u6838\u5b9e', u'\u5305', u'\u8ddf\u8fdb', u'\u6211\u53f8', u'\u95ee\u9898', u'\u79f0', u'\u4f7f\u7528', u'\u76f8\u5173', u'\u4e2d\u5fc3', u'\u7ecf', u'\u8bf7', u'\u5355', u'\u8303\u56f4', u'\u8c22\u8c22', u'\u529e\u7406', u'\u5305', u'\u6ca1\u6709', u'\u89e3\u91ca', u'\u662f', u'\u53cd\u6620', u'\u5230', u'\u6709', u'\u6838\u5b9e', u'\u8ddf\u8fdb', u'\u56de\u590d', u'\u8868\u793a', u'\u95ee\u9898', u'\u65e0\u6cd5', u'\u5185\u5bb9', u'\u76f8\u5173', u'\u63a5\u53d7', u'\u8bf7', u'\u8c22\u8c22', u'\u9519', u'\u8303\u56f4', u'\u529e\u7406', u'\u53cd\u6620', u'\u89e3\u91ca', u'\u6ca1\u6709', u'\u6709', u'\u662f', u'\u6838\u5b9e', u'\u5230', u'\u8868\u793a', u'\u6211\u53f8', u'\u8ddf\u8fdb', u'\u79f0', u'\u95ee\u9898', u'\u76f8\u5173', u'\u5305', u'\u65e0\u6cd5', u'\u7ecf', u'\u63a5\u53d7', u'\u56de\u590d', u'\u90e8\u95e8', u'\u5185\u5bb9', u'\u547c', u'\u8868\u793a', u'\u4e2d\u5fc3', u'\u8c22\u8c22', u'\u4f5c', u'\u8bf7', u'\u63a5\u53d7', u'\u8bf7', u'\u503c', u'\u67e5\u6838', u'\u6709', u'\u7231\u5fc3', u'\u4f1a', u'\u4f5c\u5f0a', u'\u63a5\u53d7', u'\u5982', u'\u662f', u'\u5c0f\u59d0', u'\u65e0\u6cd5', u'\u51fa\u73b0', u'\u96c6\u7231', u'\u9752\u6625\u5e74\u534e', u'\u5e2e', u'\u5fc3\u610f', u'\u7231', u'\u8c22\u8c22', u'\u8981', u'\u56de\u590d', u'\u673a', u'\u8d56', u'\u53c2\u4e0e\u8005', u'\u53c2\u52a0', u'\u7231\u673a', u'\u64cd\u4f5c', u'\u62ff', u'\u95ee\u9898', u'\u8bf7', u'\u663e\u793a', u'\u7ec4', u'\u8c22\u8c22', u'\u53cd\u6620', u'\u65e0\u6cd5', u'\u662f', u'\u5185\u5bb9', u'\u89e3\u91ca', u'\u8868\u793a', u'\u4f7f\u7528', u'\u6838\u5b9e', u'\u529e\u7406', u'\u8ddf\u8fdb', u'\u63a5\u53d7', u'\u6709', u'\u6ca1\u6709', u'\u4e89\u8bae', u'\u5230', u'\u56de\u590d', u'\u76f8\u5173', u'\u95ee\u9898', u'\u5305', u'\u89e3\u91ca', u'\u529e\u7406', u'\u8bf7', u'\u8c22\u8c22', u'\u662f', u'\u6838\u5b9e', u'\u4f1a', u'\u4e2d\u5fc3', u'\u6709', u'\u7ed9\u4e88', u'\u5185\u5bb9', u'\u5e02', u'\u5230', u'\u90e8\u95e8', u'\u65e0\u6cd5', u'\u81f4\u7535', u'\u8bf7', u'\u529e\u7406', u'\u8c22\u8c22', u'\u65e0\u6cd5', u'\u662f', u'\u89e3\u91ca', u'\u6838\u5b9e', u'\u8868\u793a', u'\u53cd\u6620', u'\u95ee\u9898', u'\u6ca1\u6709', u'\u4e2a\u4eba', u'\u5185\u5bb9', u'\u5230', u'\u8ddf\u8fdb', u'\u63a5\u53d7', u'\u4e89\u8bae', u'\u6709', u'\u4f7f\u7528', u'\u76f8\u5173', u'\u56de\u590d', u'\u5355', u'\u95ee\u9898', u'\u8bf7', u'\u8c22\u8c22', u'\u53cd\u6620', u'\u8868\u793a', u'\u6838\u5b9e', u'\u6ca1\u6709', u'\u6211\u53f8', u'\u8ddf\u8fdb', u'\u5230', u'\u662f', u'\u89e3\u91ca', u'\u65e0\u6cd5', u'\u79f0', u'\u76f8\u5173', u'\u529e\u7406', u'\u5185\u5bb9', u'\u6709', u'\u56de\u590d', u'\u6536\u5230', u'\u63a5\u53d7', u'\u7f16\u53f7', u'\u544a\u77e5', u'\u5355', u'\u5305', u'\u770b\u5230', u'\u8bf7', u'\u53cd\u6620', u'\u6709', u'\u8d35\u90e8', u'\u7ec4', u'\u8c22\u8c22', u'\u95ee\u9898', u'\u529e\u7406', u'\u662f\u5426', u'\u6838\u5b9e', u'\u4e89\u8bae', u'\u65b9\u9762', u'\u56de\u590d', u'\u8bf7\u4e3a', u'\u6ca1\u6709', u'\u503e\u5411', u'\u662f', u'\u6838', u'\u8865', u'\u6001\u5ea6', u'\u9700\u8bf7', u'\u95ee\u9898', u'\u529e\u7406', u'\u8bf7', u'\u8c22\u8c22', u'\u89e3\u91ca', u'\u65e0\u6cd5', u'\u6ca1\u6709', u'\u53cd\u6620', u'\u6838\u5b9e', u'\u662f', u'\u8868\u793a', u'\u8ddf\u8fdb', u'\u5185\u5bb9', u'\u5355', u'\u76f8\u5173', u'\u53d8\u66f4', u'\u56de\u590d', u'\u63a5\u53d7', u'\u6709', u'\u5230', u'\u90e8\u95e8', u'\u4e89\u8bae', u'\u79f0', u'\u6211\u53f8', u'\u529e\u7406', u'\u8bf7', u'\u8c22\u8c22', u'\u56de\u590d', u'\u5305', u'\u89e3\u91ca', u'\u6709', u'\u6838\u5b9e', u'\u53cd\u6620', u'\u5230', u'\u8868\u793a', u'\u6ca1\u6709', u'\u4e89\u8bae', u'\u95ee\u9898', u'\u7ecf', u'\u63a5\u53d7', u'\u65e0\u6cd5', u'\u90e8', u'\u8d35\u5904', u'\u610f\u89c1', u'\u6298', u'\u662f', u'\u5355', u'\u95ee\u9898', u'\u5230', u'\u8bf7', u'\u8c22\u8c22', u'\u7ec4', u'\u6ca1\u6709', u'\u53cd\u6620', u'\u6838\u5b9e', u'\u89e3\u91ca', u'\u4e0d\u5230', u'\u8868\u793a', u'\u63a5\u53d7', u'\u6709', u'\u8ddf\u8fdb', u'\u6211\u53f8', u'\u662f', u'\u56de\u590d', u'\u79f0', u'\u5185\u5bb9', u'\u76f8\u5173', u'\u7ecf', u'\u5efa\u8bae', u'\u8bf7', u'\u95ee\u9898', u'\u6838\u5b9e', u'\u53cd\u6620', u'\u8c22\u8c22', u'\u529e\u7406', u'\u6709', u'\u6211\u53f8', u'\u8868\u793a', u'\u6ca1\u6709', u'\u56de\u590d', u'\u5355', u'\u8ddf\u8fdb', u'\u7ecf', u'\u662f', u'\u90e8\u95e8', u'\u5185\u5bb9', u'\u7f16\u53f7', u'\u5230', u'\u65e0\u6cd5', u'\u5efa\u8bae', u'\u89e3\u91ca', u'\u79f0', u'\u9700\u8981', u'\u8bf7', u'\u89e3\u91ca', u'\u529e\u7406', u'\u8c22\u8c22', u'\u6ca1\u6709', u'\u8868\u793a', u'\u6709', u'\u53cd\u6620', u'\u4e89\u8bae', u'\u6838\u5b9e', u'\u662f', u'\u5230', u'\u79f0', u'\u95ee\u9898', u'\u4f7f\u7528', u'\u63a5\u53d7', u'\u8ddf\u8fdb', u'\u65e0\u6545', u'\u8bf7', u'\u8c22\u8c22', u'\u547c', u'\u4e2d\u5fc3', u'\u6211\u53f8', u'\u53cd\u6620', u'\u529e\u7406', u'\u6709', u'\u5305', u'\u79f0', u'\u56de\u590d', u'\u9700\u8981', u'\u8ddf\u8fdb', u'\u8fdb\u884c', u'\u662f', u'\u5185\u5bb9', u'\u89e3\u91ca', u'\u90e8\u95e8', u'\u5230', u'\u62e8\u6253', u'\u76f8\u5173', u'\u8868\u793a', u'\u89e3\u91ca', u'\u8bf7', u'\u8bf4\u660e', u'\u6210\u7acb', u'\u8c22\u8c22', u'\u6ca1\u6709', u'\u53cd\u6620', u'\u662f', u'\u529e\u7406', u'\u6709', u'\u8868\u793a', u'\u95ee\u9898', u'\u544a\u77e5', u'\u6211\u53f8', u'\u79f0', u'\u4f7f\u7528', u'\u63a5\u53d7', u'\u8ddf\u8fdb', u'\u6536\u5230', u'\u5185\u5bb9', u'\u81f4\u7535', u'\u65e0\u6cd5', u'\u5230', u'\u89e3\u91ca', u'\u8bf7', u'\u8bf4\u660e', u'\u6210\u7acb', u'\u529e\u7406', u'\u8c22\u8c22', u'\u662f', u'\u53cd\u6620', u'\u544a\u77e5', u'\u6ca1\u6709', u'\u79f0', u'\u95ee\u9898', u'\u6709', u'\u8868\u793a', u'\u63a5\u53d7', u'\u7ecf', u'\u4f7f\u7528', u'\u8ddf\u8fdb', u'\u65e0\u6cd5', u'\u5185\u5bb9', u'\u90e8\u95e8', u'\u56de\u590d', u'\u76f8\u5173', u'\u8bf7', u'\u8c22\u8c22', u'\u529e\u7406', u'\u53cd\u6620', u'\u95ee\u9898', u'\u89e3\u91ca', u'\u6ca1\u6709', u'\u8868\u793a', u'\u6709', u'\u8ddf\u8fdb', u'\u662f', u'\u63a5\u53d7', u'\u6211\u53f8', u'\u6536\u5230', u'\u4f7f\u7528', u'\u56de\u590d', u'\u5185\u5bb9', u'\u5230', u'\u76f8\u5173', u'\u65e0\u6cd5', u'\u4e89\u8bae', u'\u79f0', u'\u7ecf', u'\u6709', u'\u662f', u'\u8868\u793a', u'\u76f8\u5173', u'\u89e3\u91ca', u'\u6838\u5b9e', u'\u8bf4', u'\u8c22\u8c22', u'\u8bf4\u660e', u'\u67e5', u'\u8bf7', u'\u4e89\u8bae', u'\u6210\u7acb', u'\u6709', u'\u6536\u5230', u'\u89e3\u91ca', u'\u53cd\u6620', u'\u6211\u53f8', u'\u56de\u590d', u'\u6ca1\u6709', u'\u662f', u'\u53d1\u9001', u'\u6838\u5b9e', u'\u9ed1\u8272', u'\u8c22\u8c22', u'\u90ae\u5bc4', u'\u7ecf', u'\u8bf4\u660e', u'\u4e0d\u5230', u'\u627e', u'\u8bf7', u'\u8c22\u8c22', u'\u529e\u7406', u'\u53cd\u6620', u'\u89e3\u91ca', u'\u8ddf\u8fdb', u'\u6709', u'\u662f', u'\u95ee\u9898', u'\u6211\u53f8', u'\u5230', u'\u65e0\u6cd5', u'\u6ca1\u6709', u'\u8868\u793a', u'\u4f7f\u7528', u'\u63a5\u53d7', u'\u7ecf', u'\u5185\u5bb9', u'\u6838\u5b9e', u'\u76f8\u5173', u'\u8bf7', u'\u8c22\u8c22', u'\u53cd\u6620', u'\u6ca1\u6709', u'\u8868\u793a', u'\u539f\u56e0', u'\u76f8\u5173', u'\u529e\u7406', u'\u6536\u5230', u'\u90e8\u95e8', u'\u7ecf', u'\u662f', u'\u6211\u53f8', u'\u8ddf\u8fdb', u'\u6709', u'\u5230', u'\u95ee\u9898', u'\u4f7f\u7528', u'\u89e3\u91ca', u'\u5185', u'\u529e\u7406', u'\u5355', u'\u8bf7', u'\u95ee\u9898', u'\u53d8\u66f4', u'\u5185\u5bb9', u'\u65f6\u95f4', u'\u8c22\u8c22', u'\u8868\u793a', u'\u7248', u'\u7ecf', u'\u662f', u'\u4e89\u8bae', u'\u6211\u53f8', u'\u89e3\u91ca', u'\u8ddf\u8fdb', u'\u53cd\u6620', u'\u63a5\u53d7', u'\u6709', u'\u6838\u5b9e', u'\u8bf7', u'\u95ee\u9898', u'\u6ca1\u6709', u'\u8c22\u8c22', u'\u53cd\u6620', u'\u89e3\u91ca', u'\u662f', u'\u8868\u793a', u'\u6709', u'\u8ddf\u8fdb', u'\u5230', u'\u56de\u590d', u'\u79f0', u'\u5355', u'\u529e\u7406', u'\u6838\u5b9e', u'\u6536\u5230', u'\u76f8\u5173', u'\u63a5\u53d7', u'\u5185\u5bb9', u'\u6211\u53f8', u'\u65f6\u95f4', u'\u65e0', u'\u5bfc\u81f4', u'\u8fdb\u884c', u'\u89e3\u91ca', u'\u8ddf\u8fdb', u'\u53cd\u6620', u'\u4f7f\u7528', u'\u662f', u'\u5230', u'\u6237', u'\u7ed9\u4e88', u'\u5efa\u8bae', u'\u8c22\u8c22', u'\u65e0\u6cd5', u'\u95ee\u9898', u'\u8ba4\u4e3a', u'\u65f6\u6bb5', u'\u6682\u65e0', u'\u81f4\u7535', u'\u53ef', u'\u8bf7', u'\u65f6', u'\u63a5\u53d7', u'\u8bf7', u'\u529e\u7406', u'\u8c22\u8c22', u'\u89e3\u91ca', u'\u53cd\u6620', u'\u95ee\u9898', u'\u6ca1\u6709', u'\u63a5\u53d7', u'\u6709', u'\u6211\u53f8', u'\u8868\u793a', u'\u4e89\u8bae', u'\u662f', u'\u56de\u590d', u'\u8ddf\u8fdb', u'\u5230', u'\u5185\u5bb9', u'\u65e0\u6cd5', u'\u7ecf', u'\u6536\u5230', u'\u4f7f\u7528', u'\u6838\u5b9e', u'\u529e\u7406', u'\u53d8\u66f4', u'\u4e2d\u5fc3', u'\u65f6\u95f4', u'\u65e0\u6545', u'\u56de\u590d', u'\u8868\u793a', u'\u5185', u'\u89e3\u91ca', u'\u6025\u9700', u'\u6709', u'\u89e3\u9664', u'\u7ecf', u'\u95ee\u9898', u'\u6ca1\u6709', u'\u4e89\u8bae', u'\u8ddf\u8fdb', u'\u89e3\u91ca', u'\u95ee\u9898', u'\u63a5\u53d7', u'\u6237', u'\u89e3\u51b3\u95ee\u9898', u'\u7ed9\u4e88', u'\u5efa\u8bae', u'\u8c22\u8c22', u'\u6ca1\u80fd', u'\u62e8\u6253', u'\u81f4\u7535', u'\u53ef', u'\u5185\u5bb9', u'\u8bf7', u'\u539f\u56e0', u'\u8bf7', u'\u8c22\u8c22', u'\u9f99', u'\u6ca1\u6709', u'\u53cd\u6620', u'\u95ee\u9898', u'\u529e\u7406', u'\u8ddf\u8fdb', u'\u4e89\u8bae', u'\u89e3\u91ca', u'\u662f', u'\u6709', u'\u8868\u793a', u'\u6838\u5b9e', u'\u5185\u5bb9', u'\u56de\u590d', u'\u5355', u'\u539f\u56e0', u'\u5230', u'\u7ecf', u'\u4e2d\u5fc3', u'\u6536\u5230', u'\u6211\u53f8', u'\u76f8\u5173', u'\u6237', u'\u5185\u5bb9', u'\u65e0\u6cd5', u'\u9700\u8981', u'\u53cd\u6620', u'\u81f4\u6b49', u'\u6536\u5230', u'\u89e3\u91ca', u'\u610f\u89c1', u'\u79f0\u6709', u'\u529e\u7406', u'\u8ba4\u4e3a', u'\u63a5\u53d7', u'\u5305', u'\u95ee\u9898', u'\u4e89\u8bae', u'\u8bf7', u'\u529e\u7406', u'\u89e3\u91ca', u'\u8c22\u8c22', u'\u65e0\u6545', u'\u6ca1\u6709', u'\u53cd\u6620', u'\u6709', u'\u8868\u793a', u'\u65b9\u7565', u'\u8ddf\u8fdb', u'\u63a5\u53d7', u'\u662f', u'\u6211\u53f8', u'\u4e2d\u5fc3', u'\u6838\u5b9e', u'\u7ecf', u'\u5185\u5bb9', u'\u6ca1\u6709', u'\u5bfc\u81f4', u'\u8bf7', u'\u65e0\u6cd5', u'\u5904\u4e8e', u'\u8868\u793a', u'\u53cd\u6620', u'\u6709', u'\u662f', u'\u5230', u'\u610f\u89c1', u'\u76f8\u5173', u'\u6536\u53d6', u'\u8c22\u8c22', u'\u90e8\u95e8', u'\u5355', u'\u8981', u'\u4ea7\u751f', u'\u89e3\u91ca', u'\u5982', u'\u76f8\u5173', u'\u4e2a\u4eba', u'\u8d39', u'\u8c22\u8c22', u'\u4e89\u8bae', u'\u7ecf', u'\u4e0d\u7528', u'\u8bf4\u660e', u'\u90e8\u95e8', u'\u529e\u7406', u'\u79f0', u'\u8bf4', u'\u8bf7', u'\u65f6', u'\u6210\u7acb', u'\u63a5\u53d7', u'\u4e0d\u4f1a', u'\u8bf7', u'\u529e\u7406', u'\u65e0\u6cd5', u'\u8c22\u8c22', u'\u53cd\u6620', u'\u6838\u5b9e', u'\u6ca1\u6709', u'\u95ee\u9898', u'\u5185\u5bb9', u'\u662f', u'\u5230', u'\u76f8\u5173', u'\u8868\u793a', u'\u90e8\u95e8', u'\u89e3\u91ca', u'\u56de\u590d', u'\u6211\u53f8', u'\u6709', u'\u7ecf', u'\u7f51\u4e0a', u'\u5305', u'\u4f7f\u7528', u'\u8ddf\u8fdb', u'\u8c22\u8c22', u'\u8bf7', u'\u8868\u793a', u'\u8ddf\u8fdb', u'\u4e2d\u5fc3', u'\u5b89\u88c5', u'\u6ca1\u6709', u'\u5148\u751f', u'\u6838\u5bf9', u'\u529e\u7406', u'\u65e0', u'\u7f51\u4e0a', u'\u5e94\u7b54', u'\u79f0', u'\u5b89\u88c5', u'\u79f0', u'\u6cc4\u9732', u'\u6709', u'\u4fdd\u62a4', u'\u662f', u'\u5305', u'\u53cd\u6620', u'\u6211\u53f8', u'\u65b9\u9762', u'\u56de\u590d', u'\u4f7f\u7528', u'\u76f8\u5173', u'\u89e3\u91ca', u'\u505a\u597d', u'\u6ca1\u6709', u'\u6280\u672f', u'\u7535', u'\u7ed9\u4e88', u'\u8c22\u8c22', u'\u529e\u7406', u'\u6838\u5b9e', u'\u8c22\u8c22', u'\u53cd\u6620', u'\u8bf7', u'\u6001\u5ea6', u'\u5dee', u'\u89e3\u91ca', u'\u6838\u5b9e', u'\u529e\u7406', u'\u63a5\u53d7', u'\u95ee\u9898', u'\u8868\u793a', u'\u56de\u590d', u'\u8ddf\u8fdb', u'\u7ecf', u'\u7f51\u4e0a', u'\u81f4\u7535', u'\u4e2d\u5fc3', u'\u9053\u6b49', u'\u65f6\u5019', u'\u9700\u8981', u'\u8fdb\u884c', u'\u6ca1\u6709', u'\u529e\u7406', u'\u8bf7', u'\u8c22\u8c22', u'\u65e0\u6cd5', u'\u4e2d\u5fc3', u'\u4eba', u'\u8ddf\u8fdb', u'\u95ee\u9898', u'\u9700\u8981', u'\u65e0', u'\u539f\u56e0', u'\u53cd\u6620', u'\u56de\u590d', u'\u5355', u'\u89e3\u91ca', u'\u8d35\u90e8', u'\u662f', u'\u53cd\u6094', u'\u8bf7', u'\u8c22\u8c22', u'\u529e\u7406', u'\u53cd\u6620', u'\u95ee\u9898', u'\u9700\u8981', u'\u8868\u793a', u'\u4e2d\u5fc3', u'\u5b89\u88c5', u'\u65e0\u6cd5', u'\u662f', u'\u8ddf\u8fdb', u'\u89e3\u51b3', u'\u8d35\u90e8', u'\u89e3\u91ca', u'\u6ca1\u6709', u'\u65e0', u'\u4eba', u'\u56de\u590d', u'\u53cd\u9988', u'\u95ee\u9898', u'\u5305', u'\u53cd\u6620', u'\u6211\u53f8', u'\u89e3\u91ca', u'\u8bf7', u'\u4e70', u'\u7b54\u590d', u'\u7f51\u4e0a', u'\u53d1\u73b0', u'\u5e03', u'\u5982', u'\u9000', u'\u770b', u'\u6536\u5230', u'\u89e3\u51b3', u'\u5e26\u6765', u'\u62b1\u6b49', u'\u8ddf\u8fdb', u'\u5b89\u88c5', u'\u76f8\u5173', u'\u6709', u'\u544a\u77e5', u'\u8c22\u8c22', u'\u8c22\u8c22', u'\u6211\u53f8', u'\u6536\u5230', u'\u8bf7', u'\u7f51\u4e0a', u'\u8ddf\u8fdb', u'\u662f', u'\u663e\u793a', u'\u5305', u'\u8c22\u8c22', u'\u4f1a', u'\u4ea7\u751f', u'\u5e2e', u'\u7f16\u7801', u'\u6709', u'\u51fa\u73b0', u'\u529e\u7406', u'\u5bfc\u81f4\u7cfb\u7edf', u'\u6ca1\u6709', u'\u7b54\u590d', u'\u8bf7', u'\u4e89\u8bae', u'\u8bf7', u'\u529e\u7406', u'\u8c22\u8c22', u'\u65e0\u6cd5', u'\u53cd\u6620', u'\u662f', u'\u5230', u'\u6838\u5b9e', u'\u5185\u5bb9', u'\u89e3\u91ca', u'\u95ee\u9898', u'\u6ca1\u6709', u'\u8868\u793a', u'\u8ddf\u8fdb', u'\u6709', u'\u8fbe\u6807', u'\u4e2d\u5fc3', u'\u7ecf', u'\u7f51\u4e0a', u'\u8868\u793a', u'\u5305', u'\u53cd\u6620', u'\u4e2d\u5fc3', u'\u4f7f\u7528', u'\u6ca1\u6709', u'\u63a8', u'\u544a\u77e5', u'\u6253\u5f00', u'\u8c22\u8c22', u'\u6709', u'\u529e\u6cd5', u'\u5e94\u8be5', u'\u662f\u5426', u'\u8bf7', u'\u65e0\u6cd5', u'\u8bf7', u'\u8c22\u8c22', u'\u89e3\u91ca', u'\u53cd\u6620', u'\u8868\u793a', u'\u6838\u5b9e', u'\u63a5\u53d7', u'\u529e\u7406', u'\u5185\u5bb9', u'\u8ddf\u8fdb', u'\u95ee\u9898', u'\u662f', u'\u6ca1\u6709', u'\u6237', u'\u7f51\u4e0a', u'\u5230', u'\u5305', u'\u5efa\u8bae', u'\u56de\u590d', u'\u7ecf', u'\u6709', u'\u663e\u793a', u'\u65f6', u'\u8bf7', u'\u8c22\u8c22', u'\u4e2d\u5fc3', u'\u53cd\u6620', u'\u547c', u'\u8d35\u90e8', u'\u90e8\u95e8', u'\u8fdb\u884c', u'\u9700\u8981', u'\u5185\u5bb9', u'\u9700', u'\u6211\u53f8', u'\u6536\u5230', u'\u6709', u'\u5355\u4eba', u'\u63a5\u53d7', u'\u8868\u793a', u'\u95ee\u9898', u'\u51fa', u'\u8ddf\u8fdb', u'\u5f39', u'\u662f', u'\u76f8\u5173', u'\u79f0', u'\u8bf7', u'\u89e3\u91ca', u'\u8c22\u8c22', u'\u65e0\u6cd5', u'\u53cd\u6620', u'\u662f', u'\u5185\u5bb9', u'\u529e\u7406', u'\u95ee\u9898', u'\u63a5\u53d7', u'\u8868\u793a', u'\u6ca1\u6709', u'\u6838\u5b9e', u'\u8ddf\u8fdb', u'\u6211\u53f8', u'\u7f51\u4e0a', u'\u663e\u793a', u'\u76f8\u5173', u'\u6709', u'\u5230', u'\u6237', u'\u7ecf', u'\u5efa\u8bae', u'\u4f7f\u7528', u'\u529e\u7406', u'\u8bf7', u'\u8c22\u8c22', u'\u5305', u'\u53cd\u6620', u'\u8868\u793a', u'\u89e3\u91ca', u'\u662f', u'\u4e2d\u5fc3', u'\u6ca1\u6709', u'\u6709', u'\u4e89\u8bae', u'\u6838\u5b9e', u'\u95ee\u9898', u'\u5185\u5bb9', u'\u90e8\u95e8', u'\u5230', u'\u76f8\u5173', u'\u7ecf', u'\u8ddf\u8fdb', u'\u9700\u8981', u'\u56de\u590d', u'\u6536\u5230', u'\u9700', u'\u8ddf\u8fdb', u'\u4f1a', u'\u5305\u62ec', u'\u5355\u4eba', u'\u9644\u4ef6', u'\u90e8\u95e8', u'\u4f5c', u'\u79f0', u'\u5185\u5bb9', u'\u8bf7', u'\u65f6', u'\u529e\u7406', u'\u8868\u793a', u'\u8ddf\u8fdb', u'\u81f4\u6b49', u'\u9700\u8981', u'\u65f6\u95f4', u'\u4f7f\u7528', u'\u9519', u'\u89e3\u91ca', u'\u6ca1\u6709', u'\u610f\u89c1', u'\u7ed9\u4e88', u'\u5dee\u9519', u'\u9020\u6210', u'\u7b54\u590d', u'\u5185\u5bb9', u'\u8bf7', u'\u65e0\u6cd5', u'\u529e\u7406', u'\u65e0\u6cd5', u'\u5230', u'\u7ecf', u'\u79f0', u'\u5bfc\u81f4', u'\u8ddf\u8fdb', u'\u53cd\u6620', u'\u6211\u53f8', u'\u4e0b', u'\u67e5', u'\u5efa\u8bae', u'\u8c22\u8c22', u'\u8bd5', u'\u533a', u'\u65e0\u6cd5', u'\u8bf7', u'\u89e3\u91ca', u'\u8c22\u8c22', u'\u5185\u5bb9', u'\u8ddf\u8fdb', u'\u63a5\u53d7', u'\u53cd\u6620', u'\u8868\u793a', u'\u95ee\u9898', u'\u5efa\u8bae', u'\u662f', u'\u663e\u793a', u'\u7f51\u4e0a', u'\u4f7f\u7528', u'\u6ca1\u6709', u'\u529e\u7406', u'\u7ed9\u4e88', u'\u610f\u89c1', u'\u5230', u'\u76f8\u5173', u'\u56de\u590d', u'\u6211\u53f8', u'\u6838\u5b9e', u'\u6838\u5b9e', u'\u95ee\u9898', u'\u5230', u'\u53cd\u9988', u'\u5efa\u8bae', u'\u76f8\u5173', u'\u662f', u'\u79f0', u'\u8c22\u8c22', u'\u5355', u'\u6ca1\u6709', u'\u5185\u5bb9', u'\u8868\u793a', u'\u53cd\u6620', u'\u5206', u'\u6709', u'\u6536\u5230', u'\u89e3\u91ca', u'\u7f16\u53f7', u'\u544a\u77e5', u'\u8bf7', u'\u65e0\u6cd5', u'\u8c22\u8c22', u'\u529e\u7406', u'\u89e3\u91ca', u'\u662f', u'\u4f7f\u7528', u'\u8ddf\u8fdb', u'\u53cd\u6620', u'\u6211\u53f8', u'\u6838\u5b9e', u'\u76f8\u5173', u'\u5185\u5bb9', u'\u6709', u'\u56de\u590d', u'\u7ed9\u4e88', u'\u5e94\u7528', u'\u8868\u793a', u'\u5efa\u8bae', u'\u8bf7', u'\u8c22\u8c22', u'\u6ca1\u6709', u'\u5230', u'\u89e3\u91ca', u'\u65e0\u6cd5', u'\u53cd\u6620', u'\u662f', u'\u6838\u5b9e', u'\u8868\u793a', u'\u6709', u'\u63a5\u53d7', u'\u79f0', u'\u95ee\u9898', u'\u7ecf', u'\u8ddf\u8fdb', u'\u76f8\u5173', u'\u5355', u'\u6211\u53f8', u'\u90e8\u95e8', u'\u5efa\u8bae', u'\u56de\u590d', u'\u5305', u'\u89e3\u91ca', u'\u6ca1\u6709', u'\u81f4\u7535', u'\u8bf7', u'\u8ddf\u8fdb', u'\u8868\u793a', u'\u9700', u'\u53cd\u6620', u'\u5355\u4eba', u'\u6211\u53f8', u'\u610f\u89c1', u'\u5230', u'\u673a', u'\u8c22\u8c22', u'\u9a6c\u5148\u751f', u'\u529e\u7406', u'\u4ec7\u6653\u73b2', u'\u5185\u5bb9', u'\u65e0\u6cd5', u'\u63a5\u53d7', u'\u539f\u56e0', u'\u65e0\u6cd5', u'\u529e\u7406', u'\u6237', u'\u8ddf\u8fdb', u'\u4e2d\u5fc3', u'\u5bfc\u81f4', u'\u89e3\u91ca', u'\u5230', u'\u65e0', u'\u56e0\u7d20', u'\u56de\u5e94', u'\u81f4\u6b49', u'\u6ca1\u6709', u'\u610f\u89c1', u'\u53d1\u9001', u'\u7ed9\u4e88', u'\u5efa\u8bae', u'\u5b89\u629a', u'\u65f6\u95f4', u'\u5185\u5bb9', u'\u65e0\u6cd5', u'\u89e3\u91ca', u'\u53cd\u6620', u'\u63a5\u53d7', u'\u9700\u8981', u'\u575a\u6301', u'\u6237', u'\u56de\u590d', u'\u7ed9\u4e88', u'\u95ee\u9898', u'\u8bf7', u'\u5efa\u8bae', u'\u8c22\u8c22', u'\u663e\u793a', u'\u5185', u'\u53d1\u9001', u'\u610f\u89c1', u'\u7b54\u590d', u'\u5230', u'\u8bf7', u'\u8c22\u8c22', u'\u4e0d\u5230', u'\u6ca1\u6709', u'\u53cd\u6620', u'\u89e3\u91ca', u'\u6838\u5b9e', u'\u8868\u793a', u'\u6211\u53f8', u'\u63a5\u53d7', u'\u6709', u'\u8ddf\u8fdb', u'\u662f', u'\u76f8\u5173', u'\u7ecf', u'\u95ee\u9898', u'\u5185\u5bb9', u'\u79f0', u'\u7f51\u4e0a', u'\u89e3\u91ca', u'\u79f0', u'\u8c22\u8c22', u'\u63a5\u53d7', u'\u6ca1\u6709', u'\u5148\u751f', u'\u95ee\u9898', u'\u5355', u'\u6838\u5b9e', u'\u8bf7', u'\u65f6\u95f4', u'\u56de\u590d', u'\u5230', u'\u7ecf', u'\u8d39', u'\u9700\u8981', u'\u6709', u'\u7ed9\u4e88', u'\u70e6\u8bf7', u'\u6211\u53f8', u'\u5982', u'\u65e0\u4eba', u'\u6ca1', u'\u663e\u793a', u'\u8bf7', u'\u662f', u'\u65e0\u6cd5', u'\u8868\u793a', u'\u53cd\u6620', u'\u8c22\u8c22', u'\u6709', u'\u95ee\u9898', u'\u89e3\u91ca', u'\u529e\u7406', u'\u6211\u53f8', u'\u5230', u'\u56de\u590d', u'\u5185\u5bb9', u'\u51fa\u73b0', u'\u4f1a', u'\u7248',]
    result = defaultdict(int)
    seg_list = pseg.cut(line)
    for word, flag in seg_list:
        if word in stop_words:
            continue
        if flag in ['n', 'nr', 'ns', 'nz', 'nl', 'ng', 's', 'v']:
            result[word] += 1
    return result


def set_deep_dict_value(org_dict, keys, value):
    copy_keys = copy.copy(keys)
    last_key = copy_keys.pop()
    tmp = org_dict
    for key in copy_keys:
        tmp = tmp[key]
    tmp[last_key] = value


def get_deep_dict_value(org_dict, keys):
    tmp = org_dict
    for key in keys:
        tmp = tmp[key]
    return tmp


def merge_word_count(ori_word_cnt, new_word_cnt):
    new_word_result = defaultdict(int)
    for key in set(ori_word_cnt.keys() + new_word_cnt.keys()):
        new_word_result[key] += ori_word_cnt[key]
        new_word_result[key] += new_word_cnt[key]
    return new_word_result


def estimate(total_cut_result, total_word_result, total_category_cnt, line, top_n=3):
    '''
    total_cut_result: the word count for all the target word
    Eg:
        {
            网厅: {
                掌厅积分兑换: {投诉: 2, 欠费: 3},
            },
            手机商城: {
                其他: {投诉: 2, 欠费: 3},  
            }
        }

    total_word_result: the word count in all the document
    Eg:
        {投诉: 2, 欠费: 3}

    total_category_cnt:
    Eg:
        {
            网厅: {掌厅积分兑换:10, 其他:5}
        }
    '''
    line_cut_result = cut(line)
    word_score_result = defaultdict(float)
    category_list = []
    for category_one, category_one_data in total_category_cnt.iteritems():
        for category_two, category_two_data in category_one_data.iteritems():
            category_list.append(category_two_data)
    category_cnt = sum(category_list)

    for category_one, category_one_word_result in total_cut_result.iteritems():
        for category_two, category_two_word_result in category_one_word_result.iteritems():
            category_frequence = total_category_cnt[category_one][category_two] / float(category_cnt)
            word_score_result[(category_one, category_two)] = word_score(line_cut_result, category_two, category_two_word_result, category_frequence)
    return get_top_category(word_score_result, top_n)


def get_top_category(word_score_result, top_n):
    score_result = sorted(word_score_result.items(), key=operator.itemgetter(1), reverse=True)
    for item in score_result:
        category, score = item
    return score_result[:top_n]


def word_score(line_cut, key, word_result, category_frequence):
    '''
    line_cut:
    Eg:
        {投诉: 2, 欠费: 3}

    word_result: hit for a specific word
    Eg:
        {投诉: 2, 欠费: 3}

    category_frequence: the persentage of the word
    Eg:
        0.002
    '''
    score = 1.0 * category_frequence
    total_cnt = sum([x for x in word_result.values()])
    for word, word_cnt in line_cut.iteritems():
        if word in word_result:
            score *= (word_result[word] / float(total_cnt)) ** word_cnt
    return score


def pickle_load(file_path):
    with open(file_path, 'r') as input_file:
        return json.loads(pickle.load(input_file))


def pickle_dump(data, file_path):
    with open(file_path, 'wb') as output_file:
        pickle.dump(json.dumps(data), output_file)


def print_result(result, category=1):
    start = '|'
    seperator = '----|'
    for xk, xv in result.iteritems():
        print start + '%s' % (xk)
        if 1 == category:
            print_word_frequence(xv, 1)
            continue
        for yk, yv in xv.iteritems():
            print start + seperator + ' %s' % (yk)
            if 2 == category:
                print_word_frequence(yv, 2)
                continue


def print_word_frequence(result, category):
    top_word_cnt = 100
    start = '|'
    seperator = '----|'
    sorted_re = sorted(result.items(), key=operator.itemgetter(1), reverse=True)[:top_word_cnt]
    for item in sorted_re:
        k, v = item
        print start + seperator * category + k + ':' + str(v)


def predict(line):
    total_cut_result, total_word_result, total_category_cnt = learning(category=CATEGORY)
    # print_result(total_cut_result, category)
    return estimate(total_cut_result, total_word_result, total_category_cnt, line)



if __name__ == '__main__':
    # line = '18566781877用户来电反映，其在之前有办理宽带ADSLD2263902171提速12M，至今仍未提速上去，经系统查看，其宽带因为线路超长-不支持12M，现用户要求把这个提速撤销，用户要求帮其宽带提速至6M，或者帮其核实最高能提速多少M，请核实跟进处理，谢谢！联系人：王先生联系电话：18566781877'
    line = raw_input('Please input the complain (Q for quit): ')
    while line != 'Q':
        re = predict(line)
        print '----The most possible top 3 category----'
        for item in re:
            category, score = item
            print category[0], category[1], score
        line = raw_input('Please input the complain (Q for quit): ')
    print 'bye'
