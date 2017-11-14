import json
import os
import random
import re

from collections import defaultdict
from functools import partial
from multiprocessing import Pool

import click

# Change the value below to the data file name
DATA_FILE = "fner_train.json"
# set the flag below to 1 to sample random lines
RANDOM = 0


@click.group()
def cli():
    pass


def _create_dirs():
    if not os.path.exists('mentions'):
        os.makedirs('mentions')
    if not os.path.exists('oversample'):
        os.makedirs('oversample')


@cli.command('generate-mentions')
@click.option('--input_file', type=click.Path(exists=True), default=DATA_FILE)
def generate_label_mentions(input_file):
    _create_dirs()
    with open(input_file) as f:
        for line in f:
            data = json.loads(line)
            for mention in data['mentions']:
                for label in mention['labels']:
                    with open("mentions/" + label[1:].replace("/", ".") + ".dat", "a+") as f_out:
                        f_out.write(json.dumps(data) + "\n")


@cli.command('generate-reverse-index')
@click.option('--input_file', type=click.Path(exists=True), default=DATA_FILE)
def generate_reverse_index(input_file):
    data = {}
    data_count = defaultdict(int)
    _create_dirs()
    with open(input_file) as f:
        for line in f:
            data = json.loads(line)
            for mention in data['mentions']:
                mention_name = mention['name']
                if mention_name not in data:
                    data[mention_name] = {'link': mention['link'], 'labels': []}
                data[mention_name]['labels'] = list(set(data[mention_name]['labels'] + mention['labels']))
                data_count[mention_name] += 1
    data = dict(data)
    with open('res.json', 'w') as f:
        json.dump(data, f, indent=2)
    reverse_count_index = defaultdict(list)
    for key, value in data_count.items():
        reverse_count_index[value].append(key)
    with open('res_count.json', 'w') as f:
        json.dump(reverse_count_index, f, indent=2)


def get_random_lines(file, total_bytes, n):
    data = []
    for _ in range(n):
        random_point = random.randint(0, total_bytes)
        file.seek(random_point)
        file.readline()
        data.append(file.readline())
    return data


def get_n_lines(file, total_bytes, n):
    data = []
    for _ in range(n):
        data.append(file.readline())
    return data


def get_mention_data(*args):
    if RANDOM:
        return get_random_lines(*args)
    else:
        return get_n_lines(*args)


def over_sample(entity_name, n, rindex):
    if rindex is None:
        with open('res.json') as f:
            rindex = json.load(f)
    entity = rindex.get(entity_name, {})
    labels = entity.get('labels', [])
    for label in labels:
        label_file_name = label[1:].replace("/", ".") + ".dat"
        escaped_entity_name = re.sub(r'[^A-Za-z0-9]+', '', entity_name)
        file_name = os.path.join("mentions", label_file_name)
        output_fname = os.path.join("oversample", "{}.".format(escaped_entity_name), label_file_name)
        with open(file_name) as f:
            mention_data = get_mention_data(f, n)
            over_sampled_data = []
            for line in filter(lambda x: x, mention_data):
                try:
                    data = json.loads(line)
                except ValueError:
                    mention_data = {}
                else:
                    for mention in data['mentions']:
                        if label in mention['labels']:
                            mention['name'] = entity_name
                            mention['link'] = entity['link']

                            # Substituting the entity name
                            data['tokens'] = data['tokens'][0:mention['start']]
                            data['tokens'] += [entity_name]
                            data['tokens'] += data['tokens'][mention['end']:]
                            break
                if mention_data:
                    over_sampled_data.append(json.dumps(mention_data) + '\n')
        with open(output_fname, "a+") as f:
            f.writelines(over_sampled_data)


def over_sample_entities(entities, n):
    rindex = None
    with open('res.json') as f:
        rindex = json.load(f)
    over_sample_n = partial(over_sample, n=n, rindex=rindex)
    pool = Pool()
    pool.map(over_sample_n, entities)


@cli.command('oversample')
@click.option('--threshhold', default=10, help="Oversample entities with below `threshhold` number of mentions")
@click.option('--n', default=500, help="Number of lines to oversample")
def over_sample_below_thresh(threshhold, n):
    _create_dirs()
    data = json.load(open('res_count.json'))
    for i in range(1, threshhold):
        over_sample_entities(data.get(str(i), []), n)
