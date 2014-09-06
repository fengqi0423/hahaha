from scipy.sparse import coo_matrix
from itertools import izip

def sort_coo(m):
    coo_m = m.tocoo()
    tuples = izip(coo_m.row, coo_m.col, coo_m.data)
    tuples = sorted(tuples, key=lambda x: (x[0], x[1]))
    row, col, data = zip(*tuples)
    return (coo_matrix((data,(row,col)),shape=m.shape)).tocsr()