import os

ROOT = os.path.dirname(os.path.realpath(__file__))
SEPRATOR = '#' * 20
RETRIVE_COLUMNS = ['BP', 'BQ', 'BR', 'BS', 'O', 'A']
DATA_BASE_DIR = 'data'
DATA_BASE_PATH = os.path.join(ROOT, DATA_BASE_DIR)
INPUT_FILE = '2015-01-to-03.csv'
FORMATTED_OUTPUT_FILE = 'formatted.tsv'
UNFORMATTED_OUTPUT_FILE = 'unformatted.tsv'

