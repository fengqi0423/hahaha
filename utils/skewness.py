import sys
import numpy as np
from scipy.stats import skew
from sklearn.datasets import load_svmlight_file
from statsmodels.distributions.empirical_distribution import ECDF

def feature_skewness(svmfile):
    X, y = load_svmlight_file(svmfile, zero_based = False, query_id = False)
    m, n = X.shape
    for i in range(n):
        x = np.array(X[:,i].todense())[:,0]
        ecdf = ECDF(x)
        s1 = skew(x)
        s2 = skew(np.log2(x+1))
        s3 = skew(ecdf(x))
        if np.abs(s1) < np.abs(s2):
            print "%d %f -> %f or %f" % (i+1, s1, s2, s3)
        else:
            print "[!] %d %f -> %f or %f" % (i+1, s1, s2, s3)

if __name__ == "__main__":
    filename = sys.argv[1]
    feature_skewness(filename)
