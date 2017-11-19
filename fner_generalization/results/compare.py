import csv
from os.path import join

from test_names import data_dir

def writeCsv(filename, data):
    with open(join(data_dir, filename), "w") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    

def readCsv(filename):
    with open(join(data_dir, filename)) as f:
        reader  = csv.reader(f)
        data = list(reader)
    return data



def combine(original, sample):
    data = []
    for label in original:
        old = original[label]
        new = sample[label]
        data.append([label, old[1], new[1], old[4], new[4]])
    return data

def get_new_results(filename, original):
    sample = {}
    data = readCsv(filename)
    for row in data:
        label = row[0]
        if label in original:
            sample[label] = row
    return sample

def compare_oversampling():
    original = {}
    data = readCsv("result_1.csv")
    for row in data:
        [label,mentions] = row[:2]
        if int(mentions) < 8:
            original[label] = row
                
    oversample = get_new_results("result_3.csv", original)

    final = combine(original, oversample)
    writeCsv("oversample.csv", final)

def compare_undersampling():
    original = {}
    data = readCsv("result_1.csv")
    for row in data:
        [label,mentions] = row[:2]
        if int(mentions) > 1000:
            original[label] = row

    undersample = get_new_results("result_4.csv", original)
    final = combine(original, undersample)
    writeCsv("undersample.csv", final)


def compare_combined():
    original = {}
    data = readCsv("result_1.csv")
    for row in data:
        [label,mentions] = row[:2]
        if int(mentions) > 1000 or int(mentions) < 8:
            original[label] = row
    sample = get_new_results("result_2.csv", original)
    final = combine(original, sample)
    writeCsv("combined.csv", final)


if __name__ == '__main__':
    compare_oversampling()
    compare_undersampling()
    compare_combined()
