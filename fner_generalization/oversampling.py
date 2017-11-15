import json
import os
import re

from functools import partial
from multiprocessing import Pool
from shutil import copyfileobj

import click

from fner_generalization.constants import (REVERSE_INDEX, MENTION_DIR,
                                           OVERSAMPLE_DIR, REVERSE_COUNT_INDEX,
                                           OVERSAMPLE_DATA, SAMPLE_DATA_FILE)


def get_mention_data(file, n):
    data = []
    for _ in range(n):
        data.append(file.readline())
    return data


def over_sample(entity_name, n, rindex):
    if rindex is None:
        with open(REVERSE_INDEX) as f:
            rindex = json.load(f)
    entity = rindex.get(entity_name, {})
    # print(entity_name)
    print(entity)
    labels = entity.get('labels', [])
    for label in labels:
        label_fname = label[1:].replace("/", ".") + ".dat"
        escaped_entity_name = re.sub(r'[^A-Za-z0-9]+', '', entity_name)
        file_name = os.path.join(MENTION_DIR, label_fname)
        output_fname = os.path.join(OVERSAMPLE_DIR, "{}.{}".format(escaped_entity_name, label_fname))
        with open(file_name) as f:
            mention_data = get_mention_data(f, n)
            over_sampled_data = []
            for line in filter(lambda x: x, mention_data):
                try:
                    data = json.loads(line)
                except ValueError:
                    data = {}
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
                if data:
                    over_sampled_data.append(json.dumps(data) + '\n')
        print(output_fname)
        with open(output_fname, "a+") as f:
            f.writelines(over_sampled_data)


def over_sample_entities(entities, n):
    rindex = None
    with open(REVERSE_INDEX) as f:
        rindex = json.load(f)
    over_sample_n = partial(over_sample, n=n, rindex=rindex)
    # print(entities)
    pool = Pool()
    pool.map(over_sample_n, entities)


@click.command('oversample')
@click.option('--threshhold', default=10, help="Oversample entities with below `threshhold` number of mentions")
@click.option('--n', default=500, help="Number of lines to oversample")
def over_sample_below_thresh(threshhold, n):
    data = json.load(open(REVERSE_COUNT_INDEX))
    for i in range(1, threshhold):
        over_sample_entities(data.get(str(i), []), n)


@click.command('generate-oversample-data')
@click.option('--output', type=click.Path(), default=OVERSAMPLE_DATA, help="Path to the output file")
@click.option('--datafile', type=click.Path(exists=True), default=SAMPLE_DATA_FILE, help="Path to the output file")
def generate_over_sampled_data(output, datafile):
    files = [SAMPLE_DATA_FILE]
    files.extend(os.listdir(OVERSAMPLE_DIR))
    with open(output, 'wb+') as wfd:
        for f in files:
            with open(os.path.join(OVERSAMPLE_DIR, f), 'rb') as rfd:
                copyfileobj(rfd, wfd)
