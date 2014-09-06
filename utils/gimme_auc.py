import sys
from sklearn.metrics import auc, roc_curve

def read_numbers(filename):
    ret = []
    with open(filename) as f:
        f.readline() # header
        l = f.readline()
        while l:
            ret.append(float(l))
            l = f.readline()
    print "got %d lines from %s" % (len(ret), filename)
    return ret

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: python gimme_auc.py {real_labels} {prediction_probabilities}"
    y = read_numbers(sys.argv[1])
    prob = read_numbers(sys.argv[2])
    fpr, tpr, thresholds = roc_curve(y, prob, pos_label=1)
    auc_score = auc(fpr, tpr)
    print "AUC %f" % auc_score
