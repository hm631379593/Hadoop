import sys
sys.path.append("/usr/hdp/2.5.0.0-1245/spark/python")

try:
    import numpy as np
    import scipy.sparse as sps
    from pyspark.mllib.linalg import Vectors

    dv1 = np.array([1.0, 0.0, 3.0])
    dv2 = [1.0, 0.0, 3.0]
    sv1 = Vectors.sparse(3, [0, 2], [1.0, 3.0])
    sv2 = sps.csc_matrix((np.array([1.0, 3.0]), np.array([0, 2]), np.array([0, 2])), shape=(3, 1))

    print(sv2)

except ImportError as e:
    print("Can not import Spark Modules", e)
    sys.exit(1)
