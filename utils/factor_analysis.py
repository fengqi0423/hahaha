import sys
from sklearn.decomposition import FactorAnalysis
from sklearn.datasets import load_svmlight_file, dump_svmlight_file

if __name__ == "__main__":
    svm_file = sys.argv[1]
    dim = int(sys.argv[2])
    fa = FactorAnalysis(
        n_components=dim, 
        tol=0.01, 
        copy=False,
        max_iter=1000, 
        verbose=3, 
        noise_variance_init=None,
    )

    X, y = load_svmlight_file(svm_file, zero_based = False, query_id = False)
    X_new = fa.fit_transform(X.toarray(), y)

    dump_svmlight_file(X_new, y, "%s.fa%d" % (svm_file, dim), zero_based = False)



