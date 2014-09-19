from sklearn.preprocessing import OneHotEncoder
import numpy as np
from logger import logger

def log_feature_cnt(X_trn, X_tst):
    logger.info('TRN {} features'.format(X_trn.shape[1]))
    logger.info('TST {} features'.format(X_tst.shape[1]))
    if X_trn.shape[1] != X_tst.shape[1]:
        logger.info('WARNING, feature cnt does not match!!!!')

def get_categorical_stat(trn_feature, tst_feature, trn_label, trn_idx):
    """Stats on categorical features"""
    
    smooth_up = 1
    smooth_down = 3
    local_stats = get_stat(trn_feature, trn_label, smooth_up, smooth_down, trn_idx)
    trn_cat_stats = trn_feature.apply(lambda x: get_pr(local_stats, x, smooth_up, smooth_down))

    trn_stats = get_stat(trn_feature, trn_label, smooth_up, smooth_down)
    tst_cat_stats = tst_feature.apply(lambda x: get_pr(trn_stats, x, smooth_up, smooth_down))
    return np.matrix(trn_cat_stats).reshape(len(trn_feature), 1), np.matrix(tst_cat_stats).reshape(len(tst_feature), 1)

def get_pr(stats, cat, smooth_up, smooth_down):
    pos_total = stats.get(cat, [smooth_up, smooth_down])
    return pos_total[0] / float(pos_total[1])
    
def get_stat(features, labels, smooth_up, smooth_down, idx=[]):
    stats = {}

    if len(idx)==0:
        idx=range(len(features))

    for i in idx:
        key = features[i]
        label = labels[i]
        if key not in stats:
                stats[key] = [smooth_up, smooth_down] # count of true, total
            stats[key][1] = stats[key][1] + 1
            if label == True or label == 1:
                stats[key][0] = stats[key][0] + 1
    return stats

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