import file_io
import config
from sklearn import metrics
from optparse import OptionParser
import avg_precision
from collections import defaultdict
import numpy as np
import sys

def process(test_file, index, reverse, metrics):
    test_data = file_io.read_csv('data', test_file)
    header = file_io.get_csv_header('data', test_file)
    print "Test result of feature %s Reverse %s" % (header[index]  , str(reverse))

    for metric in metrics.split(','):
        methodToCall = getattr(sys.modules[__name__], metric.rstrip())    
        methodToCall(test_data, index, reverse, test_file)

def minus_auc(Y,pred):
    return -1 * metrics.auc_score(Y, pred)  

def auc(test_data, index, reverse, test_file):
    pred = [x[index] for x in test_data]

    if reverse:
        pred = [ x * -1 for x in pred]
    testing_Y = [x[0] for x in test_data]
    print "AUC: \n%f\n" % metrics.auc_score(testing_Y, pred)    

def stat(test_data, index, reverse, test_file):
    """
    calculate mean and std of pos and neg point
    """

    actual = [x for x in test_data if x[0] > 0]
    false = [x for x in test_data if x[0] <= 0]

    print "Positive point mean : %f std : %f" % (np.mean([ x[index] for x in actual]), np.std([ x[index] for x in actual]))
    print "Negtive point mean : %f std : %f" % (np.mean([ x[index] for x in false]), np.std([ x[index] for x in false]))

def map(test_data, index, reverse, test_file):
    actual = [x for x in test_data if x[0] > 0]
    actual_author_paper = defaultdict(list)
    for row in actual:
        actual_author_paper[row[1]].append(row[2])
    pridict_author_paper = defaultdict(list)
    for i in range(0, len(test_data)):
        pridict_author_paper[test_data[i][1]].append((test_data[i][index], test_data[i][2]))

    apk = []
    for a_id in pridict_author_paper.keys():
        predict_list = [x[1] for x in sorted(pridict_author_paper[a_id], reverse=not reverse)]
        str_predict_list = "predict : " + "-".join([ str(x) for x in predict_list])
        if a_id not in actual_author_paper:
            apk.append((0, a_id, "actual: ", str_predict_list))
        else:
            apk.append((avg_precision.apk(actual_author_paper[a_id], predict_list, 10000), 
                        a_id, 
                        "actual: " + "-".join([ str(x) for x in actual_author_paper[a_id]]), 
                        str_predict_list))    
    print "MAP: \n%f\n" % np.mean([x[0] for x in apk])
    file_io.dump_csv(sorted(apk), 'data', test_file + '.testing.log')    

def main():
    configuration = config.get_config()["TRAIN"]
    parser = OptionParser()    
    parser.add_option("-e", dest="test", default="")     
    parser.add_option("--index", dest="index", default=configuration["index"][-1] + 1)  
    parser.add_option("-r", action="store_true", dest="reverse", default=False)
    parser.add_option("-m", dest="metrics", default="")
     
    (opts, args) = parser.parse_args()
    if opts.test == "":
        print "Missing input..."
        return 0
    
    process(opts.test, int(opts.index), opts.reverse, opts.metrics)

if __name__=="__main__":
    main()