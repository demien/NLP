import os
from collections import defaultdict
from constants import SEPRATOR, RETRIVE_COLUMNS, DATA_BASE_PATH, FORMATTED_OUTPUT_FILE


os.chdir(DATA_BASE_PATH)


def get_column_index(column):
    columns = _get_A_to_Z()
    columns += ['A'+i for i in _get_A_to_Z()]
    columns += ['B'+i for i in _get_A_to_Z(22)]
    return columns.index(column)


def _get_A_to_Z(n=26):
    return [unichr(i) for i in range(65, 65+n)]


def load_all_result(input_path):
    result_tree = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    with open(input_path, 'r') as input_file:
        for line in input_file:
            level_one, level_two, level_three, level_four, _, _ = line.split(SEPRATOR)
            level_one, level_two, level_three, level_four = batch_trim([level_one, level_two, level_three, level_four])
            result_tree[level_one][level_two][level_three].append(level_four)
    return result_tree


def batch_trim(data):
    return [x.strip() for x in data]


def generate_defaultdict(level, default):
    '''
    recursive create default, using 'default' as the leaf node default value
    '''
    if level <= 1:
        return defaultdict(default)
    else:
        level -= 1
        return defaultdict(lambda: generate_defaultdict(level, default))


def print_result(result, level=3):
    start = '|'
    seperator = '----|'
    for x in result.keys():
        if 1 <= level:
            print start + '%s: %s' % (x, count_dict(result[x]))
        for y in result[x].keys():
            if 2 <= level:
                print start + seperator + ' %s: %s' % (y, count_dict(result[x][y]))
            for z in result[x][y].keys():
                if 3 <= level:
                    print start + seperator * 2 + ' %s: %s' % (z, count_dict(result[x][y][z]))
                for zz in result[x][y][z]:
                    if zz:
                        if 4 <= level:
                            print start + seperator * 3 + ' %s' % (zz)


def count_dict(data):
    cnt = 0
    if type(data) == dict or type(data) == defaultdict:
        for k, v in data.iteritems():
            cnt += count_dict(v)
        return cnt
    if type(data) == list:
        return len(data)


def print_dict(data, tab_cnt=0):
    if type(data) == dict or type(data) == defaultdict:
        for k, v in data.iteritems():
            print '\t' * tab_cnt + k
            tab_cnt += 1
            print print_dict(v, tab_cnt)
    else:
        if type(data) is list:
            for k in data:
                print '\t' * tab_cnt + k
        else:
            print '\t' * tab_cnt + str(data)


if __name__ == '__main__':
    tree = load_all_result(FORMATTED_OUTPUT_FILE)
    print_result(tree, 2)
