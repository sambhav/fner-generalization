import json

from collections import defaultdict

import click

from fner_generalization.constants import (SAMPLE_DATA_FILE,
                                         REVERSE_COUNT_INDEX,
                                         UNDERSAMPLE_DATA)


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
            if under_sample:
                for name in valid:
                    if count[name] < n:
                        count[name] += 1
                result.append(json.dumps(line) + '\n')

    with open(UNDERSAMPLE_DATA, 'w') as f:
        f.writelines(result)


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
