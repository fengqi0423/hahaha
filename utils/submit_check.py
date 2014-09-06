from utils import file_io, config
from optparse import OptionParser

def process(check_file):
    standard_submission = file_io.read_csv("data_path", "sampleSubmission.csv")
    standard_header = file_io.get_csv_header("data_path", "sampleSubmission.csv")
    total_row = len(standard_submission)
    check_dic = {}
    for row in standard_submission:
        check_dic[row[0]] = False
    header = file_io.get_csv_header("data", check_file)
    if len(header) != len(standard_header):
        print "not enough item in header %s expect %d items" % (str(header), len(standard_header))
        return False
    for i in range(len(standard_header)):
        if header[i] != standard_header[i]:
            print "header issue... expect %s" % str(standard_header)
            return False

    check_data = file_io.read_csv("data", check_file)
    row_count = 0
    for row in check_data:
        if row[0] not in check_dic:            
            print "unknown key %s" % str(row)
            return False
        check_dic[row[0]] = True
        row_count += 1

    if row_count != total_row:
        print "expect %s rows, only get %s rows" % (str(total_row), str(row_count))
        return False

    for key, check_status in check_dic.items():
        if not check_status:
            print "can't find key %s in submit file" % str(key)
            return False
    return True

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-c", dest="check", default="")
    (opts, args) = parser.parse_args()
    check_result = process(opts.check)
    if check_result:
        print "pass all check"
    else:
        print "failed..."