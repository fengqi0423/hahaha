from utils import file_io, config
import random
from optparse import OptionParser

def process(data_file, method, ratio):
    configuration = config.get_config()["TRAIN"]
    data = file_io.read_raw_file(config.get_path('data', data_file), configuration["header_lines"])
    header = file_io.read_raw_header(config.get_path('data', data_file), configuration["header_lines"])
    print header
    train = [ [x] for x in header]
    print train
    test = [ [x] for x in header]
    random.seed(0)

    for row in data:        
        if put_into_training_set_1(row, ratio):
            train.append([row])
        else:
            test.append([row])

    file_io.dump_csv(train, 'data', data_file + ".train")
    file_io.dump_csv(test, 'data', data_file + ".test")
    return

def put_into_training_set_1(row, ratio):
    return random.random() > ratio

def put_into_training_set_2(row):
    return row[1] % 2 == 0

def main():
    parser = OptionParser()
    parser.add_option("-d", dest="data_file", default="") 
    parser.add_option("-m", dest="method", default="")
    parser.add_option("-r", dest="ratio", default="0.2")       
    (opts, args) = parser.parse_args()
    if opts.data_file == "":
        print "Missing input file..."
        return 0
    
    process(opts.data_file, opts.method, float(opts.ratio))

if __name__=="__main__":
    main()
