import argparse
import numpy as np
from sklearn.datasets import dump_svmlight_file
import errno, sys

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--feature-file', '-f', required=True, dest='feature_file')
    parser.add_argument('--predict-files', '-p', required=True, dest='predict_files')
    parser.add_argument('--target-file', '-t', required=False, dest='target_file', default=None)

    args = parser.parse_args()

    
    features = []
    for f in args.predict_files.split():        
        features.append(np.loadtxt(f))

    if len(features) == 0:
        sys.exit(errno.EINVAL) 
    features = np.matrix(features).transpose()

    print args.predict_files
    y = [0, ] * features.shape[0]
    if args.target_file:
        y = np.loadtxt(args.target_file)

    dump_svmlight_file(features, y, args.feature_file, zero_based=False)

