import json
import os

from collections import defaultdict
import click

from fner_generalization.constants import (DATA_DIR, MENTION_DIR,
                                           OVERSAMPLE_DIR, SAMPLE_DATA_FILE,
                                           REVERSE_INDEX, REVERSE_COUNT_INDEX,
                                           LABEL_COUNT_INDEX, REVERSE_LABEL_COUNT_INDEX)


def _create_dirs():
    dir_paths = [DATA_DIR, MENTION_DIR, OVERSAMPLE_DIR]
    for dirpath in dir_paths:
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)


@click.command('generate-mentions')
@click.option('--input_file', type=click.Path(exists=True), default=SAMPLE_DATA_FILE)
def generate_label_mentions(input_file):
    _create_dirs()
    with open(input_file) as f:
        for line in f:
            data = json.loads(line)
            for mention in data['mentions']:
                for label in mention['labels']:
                    label_fname = label[1:].replace("/", ".") + ".dat"
                    with open(os.path.join(MENTION_DIR, label_fname), "a+") as f_out:
                        f_out.write(json.dumps(data) + "\n")


@click.command('generate-reverse-index')
@click.option('--input_file', type=click.Path(exists=True), default=SAMPLE_DATA_FILE)
def generate_reverse_index(input_file):
    output_data = {}
    data_count = defaultdict(int)
    _create_dirs()
    label_count = defaultdict(lambda: defaultdict(int))
    with open(input_file) as f:
        for line in f:
            data = json.loads(line)
            for mention in data['mentions']:
                mention_name = mention['name']
                if mention_name not in output_data:
                    output_data[mention_name] = {'link': mention['link'], 'labels': []}
                output_data[mention_name]['labels'] = list(set(output_data[mention_name]['labels'] + mention['labels']))
                for label in mention['labels']:
                    label_count[mention_name][label] += 1
                data_count[mention_name] += 1
    output_data = dict(output_data)
    reverse_label_count = defaultdict(lambda: defaultdict(list))
    with open(REVERSE_INDEX, 'w') as f:
        json.dump(output_data, f, indent=2)
    reverse_count_index = defaultdict(list)
    for key, value in data_count.items():
        reverse_count_index[value].append(key)
    for key, labels in label_count.items():
        for label, count in labels.items():
            reverse_label_count[count][key].append(label)
    with open(REVERSE_COUNT_INDEX, 'w') as f:
        json.dump(reverse_count_index, f, indent=2)
    with open(LABEL_COUNT_INDEX, 'w') as f:
        json.dump(label_count, f, indent=2)
    with open(REVERSE_LABEL_COUNT_INDEX, 'w') as f:
        json.dump(reverse_label_count, f, indent=2)
