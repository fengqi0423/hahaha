import os
import argparse
from sklearn.datasets import dump_svmlight_file, load_svmlight_file
import numpy as np

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', '-i', required=True, dest='input_file')
    parser.add_argument('--output-file', '-o', required=True, dest='output_file')

    args = parser.parse_args()

    X, y = load_svmlight_file(args.input_file)

    y_hat = X.toarray().mean(axis=1)
    np.savetxt(args.output_file, y_hat, fmt='%.8f')
