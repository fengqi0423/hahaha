from sklearn.preprocessing import OneHotEncoder
import numpy as np
from logger import logger

def log_feature_cnt(X_trn, X_tst):
    logger.info('TRN {} features'.format(X_trn.shape[1]))
    logger.info('TST {} features'.format(X_tst.shape[1]))
    if X_trn.shape[1] != X_tst.shape[1]:
        logger.info('WARNING, feature cnt does not match!!!!')

def encode_categorical_feature(trn_feature, tst_feature=[], min_obs=10, n=None):
    """Encode the Pandas column into sparse matrix with one-hot-encoding."""

    if not n:
        n = len(trn_feature)

    label_encoder = get_label_encoder(trn_feature[:n], min_obs)
    trn_labels = trn_feature.apply(lambda x: label_encoder.get(x, 0))
    trn_labels = np.matrix(trn_labels).reshape(len(trn_labels), 1)
    enc = OneHotEncoder()
    trn_encode = enc.fit_transform(trn_labels)

    tst_encode = None
    if len(tst_feature) > 0:
        tst_labels = tst_feature.apply(lambda x: label_encoder.get(x, 0))
        tst_labels = np.matrix(tst_labels).reshape(len(tst_labels), 1)
        tst_encode = enc.transform(tst_labels)

    return trn_encode, tst_encode

def get_label_encoder(feature, min_obs=10):
    label_count = {}
    for label in feature:
        if label in label_count:
            label_count[label] += 1
        else:
            label_count[label] = 1

    label_encoder = {}    
    for label in label_count.keys():
        if label_count[label] >= min_obs:
            label_encoder[label] = len(label_encoder) + 1

    return label_encoder