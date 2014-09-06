import numpy

def save_in_sparse_format(data, label, header, filename, sparse_fmt=True):
    """
    data - numpy matrix of data
    label - a 1D matrix of labels, if this is none, 0 will be used
    header - will be saved as a seperate file
    """
    N, M = data.shape
    if label != None and (label.shape[0] != N):
        raise Exception("Label and data does not match.")

    with open(filename, 'w') as f:
        for i in range(N):
            if label != None:
                f.write(str(int(label[i,0])))
            else:
                f.write('0')

            for j in range(M):
                if data[i,j] != 0:
                    f.write(' ')
                    f.write("%d:%s" % (j+1, str(data[i,j])))

            f.write('\n')

    with open(filename+'.header', 'w') as f:
        for i in range(len(header)):
            f.write("%d:%s\n" % (i+1, header[i]))