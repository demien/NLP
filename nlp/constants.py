import os

ROOT = os.path.dirname(os.path.realpath(__file__))
SEPRATOR = '#' * 20
RETRIVE_COLUMNS = ['BP', 'BQ', 'BR', 'BS', 'O', 'A']
DATA_BASE_DIR = 'data'
DATA_TRAINING_RESULT_DIR = 'training_result'
DATA_BASE_PATH = os.path.join(ROOT, DATA_BASE_DIR)
DATA_TRAINING_RESULT_PATH = os.path.join(ROOT, DATA_TRAINING_RESULT_DIR)

INPUT_FILE = os.path.join(DATA_BASE_PATH, '2015-01-to-03.csv')
FORMATTED_OUTPUT_FILE = os.path.join(DATA_BASE_PATH, 'formatted.tsv')
UNFORMATTED_OUTPUT_FILE = os.path.join(DATA_BASE_PATH, 'unformatted.tsv')

PICKLE_TOTAL_CUT_RESULT = os.path.join(DATA_TRAINING_RESULT_PATH, 'pickle_total_cut_result.pkl')
PICKLE_TOTAL_WORD_RESULT = os.path.join(DATA_TRAINING_RESULT_PATH, 'pickle_total_word_result.pkl')
PICKLE_TOTAL_CATEGORY_CNT = os.path.join(DATA_TRAINING_RESULT_PATH, 'pickle_total_category_cnt.pkl')
