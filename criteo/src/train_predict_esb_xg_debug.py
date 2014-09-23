#!/usr/bin/env python

import argparse
import numpy as np
import pandas as pd
from sklearn import cross_validation, metrics
from sklearn.preprocessing import StandardScaler
import time

from kaggler.const import FIXED_SEED
from kaggler.logger import log
from kaggler.util import load_data
import xgboost as xgb


def train_predict_xg_cv(train_file, test_file, predict_train_file,
                        predict_test_file, n_iter, depth, lrate, n_fold=10):
    param = {'bst:max_depth': depth,
             'bst:eta': lrate,
             'bst:subsample': 0.5,
             'silent': 1,
             'objective': 'binary:logistic',
             'eval_metric': 'auc',
             'nthread': 4}

    log.info("reading in the training data")
    X_trn, y_trn = load_data(train_file)
    X_trn = X_trn.todense()

    log.info("reading in the test data")
    X_tst, _ = load_data(test_file)
    X_tst = X_tst.todense()

    log.info('Normalizing data')
    scaler = StandardScaler()
    X_trn = scaler.fit_transform(X_trn)
    X_tst = scaler.transform(X_tst)

    dtest = xgb.DMatrix(X_tst)

    cv = cross_validation.StratifiedKFold(y_trn, n_folds=n_fold, shuffle=True,
                                          random_state=1)

    yhat_tst = np.zeros((X_tst.shape[0], ))
    yhat_trn = np.zeros((X_trn.shape[0], ))
    for i, (i_trn, i_val) in enumerate(cv, start=1):
        log.info('Training CV #{}'.format(i))
        dtrain = xgb.DMatrix(X_trn[i_trn].copy())
        dtrain.set_label(y_trn[i_trn].copy())

        dvalid = xgb.DMatrix(X_trn[i_val].copy())
        dvalid.set_label(y_trn[i_val].copy())

        evallist = [(dvalid, 'eval'), (dtrain, 'train')]
        bst = xgb.train(param, dtrain, n_iter, evallist)

        yhat_trn[i_val] = np.array(bst.predict(dvalid))
        yhat_tst += np.array(bst.predict(dtest)) / n_fold
    
    auc_cv = metrics.roc_auc_score(y_trn, yhat_trn)
    log.info('AUC CV: {}'.format(auc_cv))
    log.info("writing test predictions to file")
    np.savetxt(predict_train_file, yhat_trn, fmt='%.6f', delimiter=',')
    np.savetxt(predict_test_file, yhat_tst, fmt='%.6f', delimiter=',')

    
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train-file', '-t', required=True, dest='train')
    parser.add_argument('--test-file', '-v', required=True, dest='test')
    parser.add_argument('--predict-train-file', '-p', required=True,
                        dest='predict_train')
    parser.add_argument('--predict-test-file', '-q', required=True,
                        dest='predict_test')
    parser.add_argument('--n-iter', '-n', required=True, type=int, dest='n_iter')
    parser.add_argument('--depth', '-d', required=True, type=int, dest='depth')
    parser.add_argument('--learn-rate', '-l', required=True, type=float, dest='lrate')

    args = parser.parse_args()

    start = time.time()
    train_predict_xg_cv(train_file=args.train,
                        test_file=args.test,
                        predict_train_file=args.predict_train,
                        predict_test_file=args.predict_test,
                        n_iter=args.n_iter,
                        depth=args.depth,
                        lrate=args.lrate)

    log.info('finished ({:.2f} sec elasped).'.format(time.time() - start))
