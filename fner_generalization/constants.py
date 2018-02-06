import os
from os.path import dirname, realpath

DATA_DIR = os.path.join(os.path.expanduser("~"), '.fnerg')
MENTION_DIR = os.path.join(DATA_DIR, 'mentions')
PROJECT_DIR = dirname(dirname(realpath(__file__)))
OVERSAMPLE_DIR = os.path.join(DATA_DIR, 'oversample')

REVERSE_INDEX = os.path.join(DATA_DIR, 'rindex.json')
REVERSE_COUNT_INDEX = os.path.join(DATA_DIR, 'rcount.json')
LABEL_COUNT_INDEX = os.path.join(DATA_DIR, 'lcount.json')
REVERSE_LABEL_COUNT_INDEX = os.path.join(DATA_DIR, 'rlcount.json')

SAMPLE_DATA_FILE = os.path.join(PROJECT_DIR, 'sample_data', 'data.json')

OVERSAMPLE_DATA = os.path.join(DATA_DIR, 'oversample.json')
UNDERSAMPLE_DATA = os.path.join(DATA_DIR, 'undersample.json')
