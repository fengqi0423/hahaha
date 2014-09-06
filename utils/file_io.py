import os
import csv
import numpy as np
from config import get_path

CSV_DELIMITER = ','
TSV_DELIMITER = '\t'

def get_csv_header(path, file_name):
    return get_header(path, file_name, CSV_DELIMITER)

def get_header(path, file_name, delimiter):
    file_path = get_path(path, file_name)
    print "Get header of %s"%file_path
    header = ""
    with open(file_path) as f:       
        header = f.readline().rstrip()
    return header.split(delimiter)

def read_csv(path, file_name, w_head = True, max_count = None):
    return read_core(path, file_name, CSV_DELIMITER, w_head, max_count)

def read_tsv(path, file_name, w_head = True, max_count = None):
    return read_core(path, file_name, TSV_DELIMITER, w_head, max_count)

def read_core(path, file_name, delimiter, w_head = True, max_count = None):
    file_path = get_path(path, file_name)
    data = read_file(file_path, delimiter, w_head, max_count)
    return data           

def read_file(file_path, delimiter, w_head = True, max_count = None):
    data = []
    print "Reading %s begin"%file_path
    count = 0;
    with open(file_path) as f:
        if w_head:
            f.readline()
        line = f.readline().rstrip() # get rid of the titles
        while line:
            line_data = [parse_as_int_then_float_then_str(val) for val in line.split(delimiter)]
            count = count + 1
            data.append(line_data)                
            line = f.readline().rstrip()
            if (count % 100000) == 0:
                print "Read %d lines"%count
            if (max_count is not None) and count >= max_count:
                break 
    print "Reading %s end"%file_path
    return data       

def read_raw_header(file_path, header_lines=1):
    return read_raw_file(file_path, 0, header_lines)

def read_raw_file(file_path, header_lines=1, max_count=None):
    data = []
    print "Reading %s begin"%file_path
    count = 0;
    with open(file_path) as f:
        for i in range(header_lines):
            f.readline()
        line = f.readline() # get rid of the titles
        while line:            
            count = count + 1
            data.append(line.rstrip())                
            line = f.readline()
            if (count % 100000) == 0:
                print "Read %d lines"%count
            if (max_count is not None) and count >= max_count:
                break 
    print "Reading %s end"%file_path
    return data       

def parse_as_int_then_float_then_str(s):
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            if s == "NA":
                return 0
            return s

def dump_matrix_with_header(headers, data, path, file_name):
    file_path = get_path(path, file_name)
    m = len(data)
    n = len(data[0])
    print headers
    print m,n,len(headers)
    assert n == len(headers)

    with open(file_path, 'w') as f:
        f.write("%s\n" % ','.join(headers))
        for i in range(m):
            for j in range(n):
                if j != 0:
                    f.write(',')
                f.write(str(data[i][j]))
            f.write('\n')

def dump_csv(rows, path, file_name):
    file_path = get_path(path, file_name)
    dump_csv_core(rows, file_path)

def dump_csv_core(rows, full_path):
    writer = csv.writer(open(full_path, "w"), lineterminator="\n")    
    writer.writerows(rows)
    print "dump to file %s end"%full_path

def dump_iterable_to_lines(iterable, filename):
    with open(filename, "w") as out:
        for line in iterable:
            out.write(str(line)+"\n")
            
