import os, sys
from datetime import datetime
from sklearn.datasets import load_svmlight_file, dump_svmlight_file
from scipy import sparse
from numpy import hstack

def read_one_svm_from_folder(folder):
    files = os.listdir(folder)
    files.sort()
    files = [os.path.join(folder, f) for f in files]
    Xs = []
    ys = []
    for f in files:
        print f
        X, y = load_svmlight_file(f, zero_based = False, query_id = False)
        print X.shape
        print y.shape
        Xs.append(X)
        ys.append(y)
    Xc = sparse.hstack(Xs)
    yc = ys[0]

    return Xc, yc

def merge_svm_in_that_folder(folder):
    files = os.listdir(folder)
    files.sort()
    files = [os.path.join(folder, f) for f in files]
    offsets = [0]
    num_data_points = -1
    for f in files:
        print f
        X, _ = load_svmlight_file(f, zero_based = False, query_id = False)
        print X.shape
        if num_data_points == -1:
            num_data_points = X.shape[0]
        else:
            assert num_data_points == X.shape[0]
        offsets.append(offsets[-1]+X.shape[1])
    print "Measured index offsets:"
    print offsets

    fds = [open(os.path.join(folder, f)) for f in files]
    out = open("merged_%s.svm" % datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"), 'w')
    for i in range(num_data_points):
        if i % 1000 == 0:
            print "Output %d data points" % i

        for j in range(len(fds)):
            offset = offsets[j]
            _line = fds[j].readline().strip(' \r\n')
            if j == 0:
                line = _line
            else:
                parts = _line.split(' ')[1:]
                offsetted = []
                for p in parts:
                    k, v = p.split(':')
                    k = int(k) + offset
                    offsetted.append("%d:%s" % (k,v))
                line += " " + " ".join(offsetted)
        out.write(line+'\n')

    for fd in fds:
        fd.close()
    out.close()

def merge_everyfile_in_that_folder(folder):
    files = os.listdir(folder)
    files.sort()
    fds = [open(os.path.join(folder, f)) for f in files]
    with open(folder+"/features_combined.csv", 'w') as outfile:
        for i in range(664099):
            line = []
            for fd in fds:
                line.append(fd.readline().strip('\n'))
            outfile.write(','.join(line)+'\n')

    for fd in fds:
        fd.close()

if __name__ == "__main__":
    folder = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == 'svm':
        merge_svm_in_that_folder(folder)
    else:
        merge_everyfile_in_that_folder(folder)

