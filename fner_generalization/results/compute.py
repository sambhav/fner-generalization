from collections import defaultdict
from os.path import dirname, realpath, join, exists
import csv
import json
import math
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


src_dir = dirname(dirname(realpath(__file__)))
data_dir = join(dirname(src_dir), "data")


def find_count(input_json, labels, data):
    count = defaultdict(int)
    with open(input_json) as f:
        for line in f:
            mentions = json.loads(line)['mentions']
            training_labels = []
            for label in mentions:
                name = label['name']
                if name in labels:
                    count[name] +=1
                
    result = []
    for label, value in count.items():
        correct = data[label]["correct"]
        incorrect = data[label]["incorrect"]
        acc = float(correct)/(correct+incorrect)
        result.append([label, value,  correct, incorrect, acc, math.log(value+1, 1.5)])
    result.sort(key=lambda x:x[1])
    return result


def accumulated_accuracy(result):
    total = 0
    accSum = 0.0
    for res in result:
        total += 1
        score = res[4]
        accSum += score 
        res.append(accSum/total)
    return result   
    
def result_with_bins(result):
    bins = {}
    for res in result:
        mentions = res[1]
        if mentions not in bins:
            bins[mentions] = {"count":0, "correct":0, "incorrect":0}
        bins[mentions]["count"] += 1
        bins[mentions]["correct"] += res[2]
        bins[mentions]["incorrect"] += res[3]
    final = []
    for key,val in bins.items():
        correct = val["correct"]
        incorrect = val["incorrect"]
        acc = float(correct)/(correct+incorrect)
        final.append([int(key),val["count"],correct,incorrect,acc,math.log(int(key)+1,1.5)])
    final.sort(key=lambda x:x[0])
    return final
  

def buildCsv(i):
    labels = set()

    with open(join(data_dir, "names_%s.json" % str(i))) as f:
        data = json.load(f)

    for label in data:
        labels.add(label)

    res = find_count(join(data_dir, "train_%s.json" % str(i)), labels, data)

    final = result_with_bins(res)

    with open(join(data_dir, "result_with_bins_%s.csv" % str(i)), 'w') as f:
        writer = csv.writer(f)
        writer.writerows(accumulated_accuracy(final))
        
    with open(join(data_dir, "result_%s.csv" % str(i)), 'w') as f:
        writer = csv.writer(f)
        writer.writerows(accumulated_accuracy(res))


# Model 1 - original
# Model 2 - Combined
# Model 3 - Oversampled
# Model 4 - Undersampled

if __name__ == '__main__':
    for i in range(1,5):
        buildCsv(i)
