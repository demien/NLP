import os
from tools import get_column_index

os.chdir('data')
CLEAN_RECORD = ''

# http://ictclas.nlpir.org/nlpir/html/readme.htm#_Toc34628484
def clean(input_path='input.csv', formatted_path='formatted.tsv', unformatted_path='unformatted.tsv'):
    formatted_records, unformatted_records = [], []
    with open(input_path, 'r') as input_file:
        record = CLEAN_RECORD
        for line in input_file:
            if _is_beginning_line(line):
                formatted_records, unformatted_records = _append_result(record, formatted_records, unformatted_records)
                record = CLEAN_RECORD
            record += line

    # last record
    formatted_records, unformatted_records = _append_result(record, formatted_records, unformatted_records)
    # print reslut
    _print_result(formatted_records, unformatted_records)
    # write to file
    _ouput_to_file(formatted_records, formatted_path)
    _ouput_to_file(unformatted_records, unformatted_path)


def _print_result(formatted_records, unformatted_records):
    print 'read %s in all' % len(formatted_records + unformatted_records)
    print 'correct %s' % len(formatted_records)
    print 'incorrect %s' % len(unformatted_records)


def _clean_record(record):
    record = record.replace('\r', '')
    record = record.replace('\n', '')
    record = _replace_comma_in_double_quotaion(record)
    return record


def _replace_comma_in_double_quotaion(record):
    split_result = record.split('\"')
    if len(split_result) == 1: # no "
        return record
    if len(split_result) % 2 == 0: # odd "
        return record
    new_record = ''
    for piece in split_result:
        if split_result.index(piece) % 2 <> 0:
            piece = piece.replace(',', '')
        new_record += piece
    return new_record


def _append_result(record, formatted_records, unformatted_records):
    record = _clean_record(record)
    if _is_formatted_record(record):
        formatted_records.append(record)
    else:
        if record:
            unformatted_records.append(record)
    return formatted_records, unformatted_records


def _ouput_to_file(records, file_name):
    with open(file_name, 'w') as output_file:
        for record in records:
            record = record.replace(',', '\t')
            record = _choose_fields(record, ['H', 'O', 'BP', 'BQ', 'BR', 'BS'])
            record += '\n'
            output_file.write(record)


def _choose_fields(record, fields=[]):
    if not fields:
        return record
    split_result = record.split('\t')
    return '\t'.join([split_result[get_column_index(field)] for field in fields])


def _is_beginning_line(line):
    try:
        if len(line) > 17 and line[16] == ',' and int(line[0:16]):
            return True
        return False
    except:
        return False


def _is_formatted_record(record):
    return len(record.split(',')) == 74


if __name__ == '__main__':
    clean('2015-01-to-03.csv')
