import argparse
import numpy as np
import os
from sklearn import metrics
import scipy as sp

def evaluate_auc(y, yhat):
    return metrics.roc_auc_score(y, yhat)

def evaluate_APatK(y, yhat, k):
    sorted_yhat = sorted(zip(range(len(yhat)), yhat), key=lambda x: x[1], reverse=True)
    
    return apk(np.where(np.array(y) >0)[0], np.array([ x[0] for x in sorted_yhat]),k)

def apk(actual, predicted, k=10):
    if len(predicted)>k:
        predicted = predicted[:k]

    score = 0.0
    num_hits = 0.0

    if actual is None:
        return 0.0

    if k <= 0:
        k = 1

    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if actual is None:
        return 0.0

    return score / min(len(actual), k)

def evaluate_ll(y, yhat):
    epsilon = 1e-15
    yhat = sp.maximum(epsilon, yhat)
    yhat = sp.minimum(1-epsilon, yhat)
    ll = sum(y*sp.log(yhat) + sp.subtract(1,y)*sp.log(sp.subtract(1,yhat)))
    ll = ll * -1.0/len(y)
    return ll

def load_data(target_file, predict_file):
    return np.loadtxt(target_file), np.loadtxt(predict_file)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--target-file', '-t', required=True, dest='target_file')
    parser.add_argument('--predict-file', '-p', required=True, dest='predict_file')

    args = parser.parse_args()

    y, yhat = load_data(target_file=args.target_file, predict_file=args.predict_file)
    auc = evaluate_auc(y=y, yhat=yhat)

    ll = evaluate_ll(y=y, yhat=yhat)

    model_name = os.path.splitext(args.predict_file)[0]
    print('auc : {0}\t{1:f}'.format(model_name, auc))
    print('ll : {0}\t{1:f}'.format(model_name, ll))
