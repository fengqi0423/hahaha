import argparse
import numpy as np
import os
import pandas as pd
from logger import logger
from utility import encode_categorical_feature, log_feature_cnt
from scipy import sparse
from sklearn.datasets import dump_svmlight_file

NUM_COLUMNS = [ 'I'+str(x) for x in range(1,14)]

CAT_COLUMNS = [ 'C'+str(x) for x in range(1,27)]

def generate_feature(train_input_file, test_input_file,
                     train_feature_file, valid_feature_file,
                     train1_feature_file, test_feature_file):
    # load data files
    logger.info('loading data files')

    trn = pd.read_csv(train_input_file)
    tst = pd.read_csv(test_input_file)

    trn.fillna(0, inplace=True)
    tst.fillna(0, inplace=True)

    # set target labels
    y_trn = np.array(trn.Label)
    y_tst = np.zeros(len(tst))
    i_trn1 = np.where(np.array(range(len(y_trn))) < len(y_trn) * ( 1 - 1.0 / 7))[0]
    i_val1 = np.where(np.array(range(len(y_trn))) >= len(y_trn) * ( 1 - 1.0 / 7))[0]

    # numerical variables
    X_trn = np.array(trn[NUM_COLUMNS])
    X_tst = np.array(tst[NUM_COLUMNS])    
    log_feature_cnt(X_trn, X_tst)

    # category variables
    for col in CAT_COLUMNS:
        logger.info('transforming feature {}'.format(col))
        
        trn_col, tst_col = encode_categorical_feature(trn[col],
                                                      tst[col],
                                                      min_obs=1000)
        X_trn = sparse.hstack((X_trn, trn_col))
        X_tst = sparse.hstack((X_tst, tst_col))
        log_feature_cnt(X_trn, X_tst)

    X_trn = X_trn.tocsr()
    X_tst = X_tst.tocsr()
    # save features as sparse matrix files
    logger.info('saving training1 features')
    dump_svmlight_file(X_trn[i_trn1], y_trn[i_trn1], train1_feature_file, zero_based=False)

    logger.info('saving val1 features')
    dump_svmlight_file(X_trn[i_val1], y_trn[i_val1], valid_feature_file, zero_based=False)

    logger.info('saving training features')
    dump_svmlight_file(X_trn, y_trn, train_feature_file, zero_based=False)

    logger.info('saving test features')
    dump_svmlight_file(X_tst, y_tst, test_feature_file, zero_based=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train-input-file', required=True,
                        dest='train_input')
    parser.add_argument('--test-input-file', required=True,
                        dest='test_input')
    parser.add_argument('--train-feature-file', required=True,
                        dest='train_feature')
    parser.add_argument('--valid-feature-file', required=True,
                        dest='valid_feature')
    parser.add_argument('--train1-feature-file', required=True,
                        dest='train1_feature')
    parser.add_argument('--test-feature-file', required=True,
                        dest='test_feature')

    args = parser.parse_args()

    generate_feature(train_input_file=args.train_input,
                     test_input_file=args.test_input,
                     train_feature_file=args.train_feature,
                     valid_feature_file=args.valid_feature,
                     train1_feature_file=args.train1_feature,
                     test_feature_file=args.test_feature)
