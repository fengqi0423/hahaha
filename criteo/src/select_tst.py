import argparse
import pandas as pd
import numpy as np
from sklearn.datasets import load_svmlight_file, dump_svmlight_file

def select_from_prediction(feature_file, pred_file, output_file, min_1, max_0):

    print "read files"
    yhat = np.loadtxt(pred_file)
    i_neg = np.where(yhat < max_0)[0]
    i_pos = np.where(yhat > min_1)[0]
    i_select = np.array(list(set(i_neg).union(set(i_pos))))
    i_select.sort()

    label = []
    cnt = 0
    positive = 0
    negative = 0
    for y in yhat:
        if y < max_0:
            label.append(0)
            negative += 1
        if y > min_1:
            label.append(1)
            positive += 1
        cnt += 1
        if cnt % 1000000 == 0:
            print "Total %d results. Find %d pos and %d neg"%(cnt, positive, negative)

    if len(i_select) != (positive + negative):
        print len(i_select)
        print positive
        print negative
        print "idx error!"
        return

    print "load for output"
    X, _ = load_svmlight_file(feature_file)
    print "dump to output"
    dump_svmlight_file(X[i_select], label, output_file, zero_based=False)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--feature-file', '-f', required=True, dest='feature_file')
    parser.add_argument('--pred-file', '-p', required=True, dest='pred_file')
    parser.add_argument('--output-file', '-o', required=True, dest='output_file')
    parser.add_argument('--threshold', '-t', required=False, dest='threshold', default=0.1)

    args = parser.parse_args()

    pr_threshold = float(args.threshold)
    min_1 = 1 - pr_threshold
    max_0 = pr_threshold

    select_from_prediction(args.feature_file, args.pred_file, args.output_file, min_1, max_0)