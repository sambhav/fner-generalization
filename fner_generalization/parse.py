import json
from collections import defaultdict

import click

from fner_generalization.constants import (TEST_DATA_FILE, RESULT_FILE,
                                            OUTPUT_FILE, TEST_DATA_COUNT_FILE,
                                            TRAIN_DATA_COUNT_FILE, TRAIN_DATA_FILE,
                                            TEMP_FILE)

def parse_test_data(test_file):
    test_data = {}
    with open(test_file) as f:
        for line in f:
            data = json.loads(line)
            key = '_'.join(map(str, (data['fileid'], data['pid'], data['senid'])))
            for mention in data['mentions']:
                mention_key = '_'.join(map(str, (key, mention['start'], mention['end'])))
                test_data[mention_key] = sorted(mention['labels'])
    return test_data

@click.command('parse-result')
@click.option('--result', type=click.Path(), default=RESULT_FILE, help="Path to the result file")
@click.option('--test_file', type=click.Path(exists=True), default=TEST_DATA_FILE, help="Path to the test file")
@click.option('--output', type=click.Path(exists=True), default=OUTPUT_FILE, help="Path to the output file")
def parse_result(result, test_file, output):
    test_data = parse_test_data(test_file)
    result_data = {}
    results = defaultdict(lambda: {'correct':0, 'incorrect':0})
    with open(result) as f:
        for line in f:
            key, labels = line.split()
            result_data[key] = sorted(labels.split(','))
    for key, test_value in test_data.items():
        if key not in result_data:
            print(f'Not Found: {key}')
        else:
            result_value = result_data[key]
            for value in test_value:
                if value in result_value:
                    results[value]['correct'] += 1
                else:
                    results[value]['incorrect'] += 1
    with open(output, 'w') as f:
        json.dump(dict(results), f, indent=2, sort_keys=True)
    with open(output+'.keys', 'w') as f:
        json.dump(list(sorted(results.keys())), f, indent=2, sort_keys=True)

@click.command('generate-missing')
@click.option('--test_count', type=click.Path(exists=True), default=TEST_DATA_COUNT_FILE, help="Path to the test file")
@click.option('--train_count', type=click.Path(exists=True), default=TRAIN_DATA_COUNT_FILE, help="Path to the test file")
@click.option('--train_data_file', type=click.Path(exists=True), default=TRAIN_DATA_FILE, help="Path to the test file")
def generate_missing(test_count, train_count, train_data_file):
    missing_low = set()
    missing = {}
    with open(test_count) as ttc, open(train_count) as trc:
        test_data = json.load(ttc)
        train_data = json.load(trc)
        for label in test_data:
            missing[label] = max(0, max(10, train_data[label]//300)- test_data[label])
            if train_data[label] < 3000:
                missing_low.add(label)
    current = set(missing.keys())
    label_data = []
    special_data = []
    with open(train_data_file) as f:
        for line in f:
            if not current:
                break
            data = json.loads(line)
            if 'mentions' in data:
                include = False
                special = False
                for mention in data['mentions']:
                    missing_labels = current & set(mention['labels'])
                    if missing_labels:
                        include = True
                        for label in missing_labels:
                            missing[label] -= 1
                            if missing[label] <= 0:
                                current.remove(label)
                        if missing_labels & missing_low:
                            special = True
                if include:
                    if special:
                        special_data.append(data)
                    else:
                        label_data.append(line)

    with open(TEMP_FILE, 'w') as f:
        f.writelines(label_data)
    with open(TEMP_FILE+'.spec', 'w') as f:
        json.dump(special_data, f, indent=2, sort_keys=True)
