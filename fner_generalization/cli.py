import click

from fner_generalization.indexing import generate_label_mentions, generate_reverse_index
from fner_generalization.oversampling import over_sample_below_thresh, generate_over_sampled_data
from fner_generalization.undersampling import under_sample_above_thresh, under_sample_entity_above_thresh

commands = {
    'generate-mentions': generate_label_mentions,
    'generate-index': generate_reverse_index,
    'oversample': over_sample_below_thresh,
    'generate-oversampled-data': generate_over_sampled_data,
    'undersample': under_sample_above_thresh,
    'undersample-entity': under_sample_entity_above_thresh,
}

fnerg = click.Group(commands=commands)
