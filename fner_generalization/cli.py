import click

from fner_generalization.indexing import generate_label_mentions, generate_reverse_index, generate_count
from fner_generalization.oversampling import over_sample_below_thresh, generate_over_sampled_data
from fner_generalization.undersampling import under_sample_above_thresh, under_sample_entity_above_thresh, under_sample_name_above_thresh
from fner_generalization.parse import parse_result, generate_missing, remove_missing

commands = {
    'generate-mentions': generate_label_mentions,
    'generate-index': generate_reverse_index,
    'oversample': over_sample_below_thresh,
    'generate-oversampled-data': generate_over_sampled_data,
    'undersample': under_sample_above_thresh,
    'undersample-entity': under_sample_entity_above_thresh,
    'undersample-name': under_sample_name_above_thresh,
    'parse-result': parse_result,
    'generate-count': generate_count,
    'generate-missing': generate_missing,
    'remove-missing': remove_missing,
}

fnerg = click.Group(commands=commands)
