import json

from collections import defaultdict

import click

from fner_generalization.constants import (SAMPLE_DATA_FILE,
                                         REVERSE_COUNT_INDEX,
                                         UNDERSAMPLE_DATA,
                                         REVERSE_LABEL_COUNT_INDEX, UNDERSAMPLE_NAME_DATA, UNDERSAMPLE_ENTITY_DATA,
                                         LABEL_COUNTS, LABEL_COUNTS_INDEX)

def under_sample_label_entities(entities, data_file):
    result = []
    with open(data_file) as f:
        for line in f:
            obj = json.loads(line)
            new_mentions = []
            for mention in obj['mentions']:
                name = mention['name']
                if name in entities:
                    name_obj = entities[name]
                    labels = set(filter(lambda x: name_obj[x] > 0, name_obj))
                    if not labels:
                        entities.pop(name)
                        continue
                    new_labels = []
                    for label in mention['labels']:
                        if label in labels:
                            name_obj[label] -= 1
                        else:
                            new_labels.append(label)
                    mention['labels'] = new_labels
                if mention['labels']:
                    new_mentions.append(mention)
            if new_mentions:
                obj['mentions'] = new_mentions
                result.append(json.dumps(obj) + '\n')
    with open(UNDERSAMPLE_ENTITY_DATA, 'w') as f:
        f.writelines(result)


def under_sample_entities(entities, n, data_file):
    en = set(entities)
    count = defaultdict(int)
    result = []
    with open(data_file) as f:
        for line in f:
            line = json.loads(line)
            mentions = line["mentions"]
            names = set([mention["name"] for mention in mentions])
            valid = names & en
            under_sample = True
            for name in valid:
                if count[name] >= n:
                    under_sample = False
            if under_sample and valid:
                for name in valid:
                    if count[name] < n:
                        count[name] += 1
            else:
                result.append(json.dumps(line) + '\n')
    with open(UNDERSAMPLE_DATA, 'w+') as f:
        f.writelines(result)

def under_sample_names(entities, data_file, flag=False):
    result = []
    en = set(entities)
    count = defaultdict(int)
    count.update(entities)
    with open(data_file) as f:
        for line in f:
            line = json.loads(line)
            mentions = line["mentions"]
            names = set([mention["name"] for mention in mentions])
            valid = names & en
            under_sample = bool(valid)
            if under_sample:
                if flag:
                    under_sample = any(map(lambda x: bool(count[x]), valid))
                else:
                    under_sample = all(map(lambda x: bool(count[x]), valid))

            if under_sample:
                for name in valid:
                    if count[name] > 0:
                        count[name] -= 1
            else:
                result.append(json.dumps(line) + '\n')
    with open(UNDERSAMPLE_NAME_DATA, 'w') as f:
        f.writelines(result)

def process_line(line, counts):
    data = json.loads(line)
    new_mentions = []
    difference = 0
    for mention in data['mentions']:
        name = mention['name']
        new_labels = []
        for label in mention['labels']:
            if counts[name][label] > 0:
                counts[name][label] -= 1
            else:
                new_labels.append(label)
        if not new_labels:
            for i in range(mention['start'], mention['end']):
                data['tokens'][i] = ''
            difference += mention['end'] - mention['start']
        else:
            mention['labels'] = new_labels
            mention['start'] -= difference
            mention['end'] -= difference
            new_mentions.append(mention)
    if not new_mentions:
        return ''
    else:
        data['mentions'] = new_mentions
        data['tokens'] = list(filter(bool, data['tokens']))
        return json.dumps(data)

@click.command('undersample')
@click.option('--threshhold', default=1000, help="Undersample entities with above `threshhold` number of mentions")
@click.option('--n', default=500, help="Number of lines to undersample")
@click.option('--data_file', type=click.Path(exists=True), default=SAMPLE_DATA_FILE)
@click.option('--index_file', type=click.Path(exists=True), default=REVERSE_COUNT_INDEX)
def under_sample_above_thresh(threshhold, n, data_file, index_file):
    data = json.load(open(index_file))
    entities = []
    for i in data:
        if int(i) >= threshhold:
            entities += data[i]
    under_sample_entities(entities, n, data_file)


@click.command('undersample-entity')
@click.option('--threshhold', default=10, help="Undersample entities with above `threshhold` number of mentions")
@click.option('--p', default=80, help="Percent of lines to undersample")
@click.option('--data_file', type=click.Path(exists=True), default=SAMPLE_DATA_FILE)
@click.option('--index_file', type=click.Path(exists=True), default=REVERSE_LABEL_COUNT_INDEX)
def under_sample_entity_above_thresh(threshhold, p, data_file, index_file):
    data = json.load(open(index_file))
    entities = defaultdict(lambda: defaultdict(int))
    for i in data:
        if int(i) >= threshhold:
            for entity, value in data[i].items():
                for label in value:
                    entities[entity][label] = int(((100.0 - p) / 100.0) * int(i))
    under_sample_label_entities(entities, data_file)

@click.command('undersample-name')
@click.option('--threshhold', default=10, help="Undersample entities with above `threshhold` number of mentions")
@click.option('--p', default=80, help="Percent of lines to undersample")
@click.option('--data_file', type=click.Path(exists=True), default=SAMPLE_DATA_FILE)
@click.option('--index_file', type=click.Path(exists=True), default=REVERSE_COUNT_INDEX)
def under_sample_name_above_thresh(threshhold, p, data_file, index_file):
    data = json.load(open(index_file))
    entities = {}
    for i in data:
        if int(i) >= threshhold:
            for entity in data[i]:
                entities[entity] = int(((100.0 - p) / 100.0) * int(i))
    under_sample_names(entities, data_file)

@click.command('undersample-new')
@click.option('--threshhold', default=3000, help="Undersample entities with above `threshhold` number of mentions")
@click.option('--data_file', type=click.Path(exists=True), default=SAMPLE_DATA_FILE)
@click.option('--index_file', type=click.Path(exists=True), default=LABEL_COUNTS_INDEX)
@click.option('--index_count_file', type=click.Path(exists=True), default=LABEL_COUNTS)
def undersample_new(threshhold, data_file, index_file, index_count_file):
    undersample_labels = {}
    undersample_data = defaultdict(lambda: defaultdict(int))
    with open(index_count_file) as f:
        data = json.load(f)
        for label, count in data.items():
            if count >= threshhold:
                undersample_labels[label] = count - threshhold
    with open(index_file) as f:
        data = json.load(f)
        for label, count in undersample_labels.items():
            label_thresh = int(undersample_labels[label]/len(data[label]))+1
            l_count = sorted(((name_count, name) for name, name_count in data[label].items()), reverse=True)
            for name_count, name in l_count:
                if name_count > label_thresh and undersample_labels[label] > 0:
                    undersample_data[name][label] = name_count - label_thresh
                    undersample_labels[label] -= name_count - label_thresh
    results = []
    with open(data_file) as f:
        for line in f:
            new_line = process_line(line, undersample_data)
            if new_line:
                results.append(new_line+'\n')
    with open(UNDERSAMPLE_DATA, 'w') as f:
        f.writelines(results)
