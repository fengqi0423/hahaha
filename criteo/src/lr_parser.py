import argparse
import pandas as pd
import numpy as np

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--lr-file', '-l', required=True, dest='lr_output_file')
    parser.add_argument('--pred-file', '-p', required=True, dest='pred_file')
    args = parser.parse_args()

    df = pd.read_csv(args.lr_output_file, sep=" ")
    np.savetxt(args.pred_file, df["1"], fmt="%f")