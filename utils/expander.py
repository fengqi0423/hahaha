import sys
import numpy
from scipy import sparse
from sklearn import datasets

mat_t = type(numpy.mat((0,0)))

def expand_categorical_feature(raw_data, columns_to_expand, header, sparse_fmt=True):
    """
    raw_data is a numpy 2D matrix or array.
    columns_to_expand is a list of columns that are treated as categorical values, and expanded to multiple columns
    header is the header strings of the raw_data
    Use at your own risk
    """
    M, N = raw_data.shape
    if sorted(columns_to_expand)[0] < 0 or columns_to_expand[-1] >= N:
        raise Exception("raw_data dimension is %d x %d, and it doesn't contain the columns %s to be expanded" % (M, N, str(columns_to_expand)))
    if not header or len(header) != N:
        raise Exception("header does not match number of dimension.")

    columns = []
    result_header = []
    for i in range(N):
        if i not in columns_to_expand:
            col = numpy.array(raw_data[:,i])
            col.shape = (M, 1)
            columns.append(col)
            result_header.append(header[i])
        else:
            h, r = expand_one_column(raw_data[:,i], header[i], sparse_fmt)
            columns.append(r)
            result_header.extend(h)
    if sparse_fmt:
        return result_header, sparse.hstack(columns, 'csr')
    else:
        return result_header, numpy.hstack(columns)

def expand_one_column(raw_data, header_prefix, sparse_fmt=True):
    data_shape = raw_data.shape    
    if len(data_shape) != 1:
        raise Exception("You should pass in a Nx1 vector.(one dimension vector)")
    M = data_shape[0]
    categories = set()
    for i in range(M):
        categories.add(raw_data[i])
    print "Going to expand column to %d columns of binary categorical data" % (len(categories))

    categories = sorted(list(categories))
    header = [header_prefix+"_"+str(c) for c in categories]

    if sparse_fmt:
        result = sparse.lil_matrix((M, len(categories)))
    else:
        result = numpy.zeros((M, len(categories)))

    cat_ind = {}
    for c in categories:
        cat_ind[c] = categories.index(c)

    for i in range(M):
        c = raw_data[i]
        result[i, cat_ind[c]] = 1

    return header, result


if __name__ == '__main__':
    m = numpy.array(range(10))
    m = numpy.vstack([m,m])
    print m.shape
    m = m.transpose()
    if len(sys.argv) > 1 and sys.argv[1] == "sparse":
        sparse_fmt = True
    else:
        sparse_fmt = False
    header, result = expand_categorical_feature(m+1, [1], ["Non_Expand", "Expanded"], sparse_fmt)
    print header
    print result
    assert result.shape == (10, 11), "wtf"
    print type(result)
    print result[:,0]

    datasets.dump_svmlight_file(result[:,1:], result[:,0], "dump.svm", False)
