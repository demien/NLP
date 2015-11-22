# encoding=utf-8
import operator
import os
from collections import defaultdict
from constants import SEPRATOR, RETRIVE_COLUMNS, DATA_BASE_PATH, FORMATTED_OUTPUT_FILE
from tools import generate_defaultdict
import jieba.posseg as pseg


os.chdir(DATA_BASE_PATH)


def learning(input_path=FORMATTED_OUTPUT_FILE):
    total_word_result = defaultdict(int)
    total_cut_result = defaultdict(lambda: defaultdict(int))
    total_category_cnt = defaultdict(int)
    cnt = 0
    with open(input_path, 'r') as input_file:
        for line in input_file:
            print cnt
            cnt += 1
            level_one, level_two, level_three, level_four, content, cid = line.split(SEPRATOR)
            line_cut_result = cut(line)
            total_word_result = merge_word_count(total_word_result, line_cut_result)
            total_cut_result[level_one] = merge_word_count(total_cut_result[level_one], cut(line))
            total_category_cnt[level_one] += 1
    return total_cut_result, total_word_result, total_category_cnt

def cut(line):
    result = defaultdict(int)
    seg_list = pseg.cut(line)
    for word, flag in seg_list:
        if flag in ['n', 'nr', 'ns', 'nz', 'nl', 'ng', 's', 'v']:
            result[word] += 1
    return result


def merge_word_count(ori_word_cnt, new_word_cnt):
    new_word_result = defaultdict(int)
    for key in set(ori_word_cnt.keys() + new_word_cnt.keys()):
        new_word_result[key] += ori_word_cnt[key]
        new_word_result[key] += new_word_cnt[key]
    return new_word_result


def estimate(total_cut_result, total_word_result, total_category_cnt, line):
    '''
    total_cut_result: the word count for all the target word
    Eg:
        {
            网厅: {投诉: 2, 欠费: 3},
            手机商城: {}
        }

    total_word_result: the word count in all the document
    Eg:
        {投诉: 2, 欠费: 3}


    total_category_cnt:
    Eg:
        {网厅:10, }
    '''
    line_cut_result = cut(line)
    word_score_result = defaultdict(float)
    category_cnt = sum(total_category_cnt.values())
    for word, word_result in total_cut_result.iteritems():
        word_frequence = total_category_cnt[word] / float(category_cnt)
        word_score_result[word] = word_score(line_cut_result, word, word_result, word_frequence)
    return get_top_category(word_score_result)


def get_top_category(word_score_result):
    score_result = sorted(word_score_result.items(), key=operator.itemgetter(1), reverse=True)
    for item in score_result:
        category, score = item
        print category, score
    return score_result[0][0]


def word_score(line_cut, word, word_result, word_frequence):
    '''
    line_cut:
    Eg:
        {投诉: 2, 欠费: 3}

    word_result: hit for a specific word
    Eg:
        {投诉: 2, 欠费: 3}

    word_frequence: the persentage of the word
    Eg:
        0.002
    '''
    score = word_frequence
    total_cnt = sum([x for x in word_result.values()])
    for word, word_cnt in line_cut.iteritems():
        if word in word_result:
            score *= (word_cnt / float(total_cnt)) ** word_cnt
    return score


if __name__ == '__main__':
    total_cut_result, total_word_result, total_category_cnt = learning()
    line = '18566781877用户来电反映，其在之前有办理宽带ADSLD2263902171提速12M，至今仍未提速上去，经系统查看，其宽带因为线路超长-不支持12M，现用户要求把这个提速撤销，用户要求帮其宽带提速至6M，或者帮其核实最高能提速多少M，请核实跟进处理，谢谢！联系人：王先生联系电话：18566781877'
    print '--------result--------'
    print estimate(total_cut_result, total_word_result, total_category_cnt, line)
