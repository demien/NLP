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
from tools import generate_defaultdict, print_result, format_keys, cd_data, cd_training_data
import jieba.posseg as pseg


CATEGORY = 2


def learning(input_path=FORMATTED_OUTPUT_FILE, category=1):
    cd_training_data()
    if os.path.isfile(PICKLE_TOTAL_CUT_RESULT) and os.path.isfile(PICKLE_TOTAL_WORD_RESULT) and \
        os.path.isfile(PICKLE_TOTAL_CATEGORY_CNT):
        return pickle_load(PICKLE_TOTAL_CUT_RESULT), pickle_load(PICKLE_TOTAL_WORD_RESULT), \
            pickle_load(PICKLE_TOTAL_CATEGORY_CNT)
    total_word_result = defaultdict(int)
    total_cut_result = generate_defaultdict(category + 1, int)
    total_category_cnt = generate_defaultdict(category, int)
    cnt = 0
    cd_data()
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

    cd_training_data()
    pickle_dump(total_cut_result, PICKLE_TOTAL_CUT_RESULT)
    pickle_dump(total_word_result, PICKLE_TOTAL_WORD_RESULT)
    pickle_dump(total_category_cnt, PICKLE_TOTAL_CATEGORY_CNT)
    return total_cut_result, total_word_result, total_category_cnt


def cut(line):
    result = defaultdict(int)
    seg_list = pseg.cut(line)
    for word, flag in seg_list:
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
    re = estimate(total_cut_result, total_word_result, total_category_cnt, line)
    print '----The most possible top 3 category----'
    for item in re:
        category, score = item
        print category[0], category[1], score



if __name__ == '__main__':
    # line = '18566781877用户来电反映，其在之前有办理宽带ADSLD2263902171提速12M，至今仍未提速上去，经系统查看，其宽带因为线路超长-不支持12M，现用户要求把这个提速撤销，用户要求帮其宽带提速至6M，或者帮其核实最高能提速多少M，请核实跟进处理，谢谢！联系人：王先生联系电话：18566781877'
    line = raw_input('Please input the complain (Q for quit): ')
    while line != 'Q':
        predict(line)
        line = raw_input('Please input the complain (Q for quit): ')
    print 'bye'
