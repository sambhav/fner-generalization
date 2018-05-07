# FNER - Generalization of data

BTP - Sambhav Kothari 


We try to improve results for fine grained entity recognition. We first prove the hypothesis that 
undermentioned entities in the training database lead to lower accuracy when testing them.

To overcome this problem we try to oversample the data by contextually replacing the entities in sentences with entities from the same class.

We also try to experiment with undersampling to further see how changes in frequency of entities in training data affect results.

# Installation
        virtualenv -p python3 venv
        source activate venv/bin/activate
        pip install click
        python run.py

# Commands
Please run `generate-mentions` and `generate-index` in that order before running any of the other commands.
```bash
Usage: run.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  generate-index
  generate-mentions
  generate-oversampled-data
  oversample
  undersample

Usage: run.py generate-index [OPTIONS]

Options:
  --input_file PATH
  --help             Show this message and exit.

Usage: run.py generate-mentions [OPTIONS]

Options:
  --input_file PATH
  --help             Show this message and exit.

Usage: run.py oversample [OPTIONS]

Options:
  --threshhold INTEGER  Oversample entities with below `threshhold` number of
                        mentions
  --n INTEGER           Number of lines to oversample
  --help                Show this message and exit.

Usage: run.py generate-oversampled-data [OPTIONS]

Options:
  --output PATH    Path to the output file
  --datafile PATH  Path to the input data file
  --help           Show this message and exit.


Usage: run.py undersample [OPTIONS]

Options:
  --threshhold INTEGER  Undersample entities with above `threshhold` number of
                        mentions
  --n INTEGER           Number of lines to undersample
  --data_file PATH
  --index_file PATH
  --help                Show this message and exit.
  
```
