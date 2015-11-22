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
    result_tree = generate_defaultdict(3, [])
    with open(input_path, 'r') as input_file:
        for line in input_file:
            level_one, level_two, level_three, level_four, _, _ = line.split(SEPRATOR)
            if level_four not in result_tree[level_one][level_two][level_three]:
                result_tree[level_one][level_two][level_three].append(level_four)
    return result_tree


def generate_defaultdict(level, default):
    '''
    recursive create default, using 'default' as the leaf node default value
    '''
    if level <= 0:
        return default
    else:
        level -= 1
        return defaultdict(lambda: generate_defaultdict(level, default))


def print_result(result, level=3):
    for x in result.keys():
        if 1 <= level:
            print x
        for y in result[x].keys():
            if 2 <= level:
                print '\t' + y 
            for z in result[x][y].keys():
                if 3 <= level:
                    print '\t\t' + z
                for zz in result[x][y][z]:
                    if zz:
                        if 4 <= level:
                            print '\t\t\t' + zz


if __name__ == '__main__':
    tree = load_all_result(FORMATTED_OUTPUT_FILE)
    print_result(tree)
