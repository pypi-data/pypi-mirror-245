from sklearn.neighbors import KNeighborsClassifier
from .__super__ import Sklearn,np


class KNN(Sklearn):
    def __init__(self):
        Sklearn.__init__(self)

    # 训练模型,数组为一行二维数组
    def training(self, arr: np.ndarray, indexs, n_neighbors=5, algorithm='auto', **kwargs):
        assert arr.shape[0] == len(indexs)
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=algorithm, **kwargs)
        self.model.fit(arr, indexs)

