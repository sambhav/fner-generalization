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
TEST_DATA_FILE = os.path.join(PROJECT_DIR, 'sample_data', 'new_mixed_test_data.json')
TRAIN_DATA_FILE = os.path.join(PROJECT_DIR, 'sample_data', 'train_data.json')
TRAIN_DATA_COUNT_FILE = os.path.join(PROJECT_DIR, 'sample_data', 'train_data_count.json')
TEST_DATA_COUNT_FILE = os.path.join(PROJECT_DIR, 'sample_data', 'test_data_count.json')
RESULT_FILE = os.path.join(PROJECT_DIR, 'sample_data', 'result.txt')
OUTPUT_FILE = os.path.join(PROJECT_DIR, 'sample_data', 'output.json')
TEMP_FILE = os.path.join(PROJECT_DIR, 'sample_data', 'temp.json')

OVERSAMPLE_DATA = os.path.join(DATA_DIR, 'oversample.json')
UNDERSAMPLE_DATA = os.path.join(DATA_DIR, 'undersample.json')
UNDERSAMPLE_NAME_DATA = os.path.join(DATA_DIR, 'undersample-name.json')
UNDERSAMPLE_ENTITY_DATA = os.path.join(DATA_DIR, 'undersample-entity.json')
