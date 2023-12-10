import sklearn.svm as svm
from .__super__ import Sklearn,np


class SVC(Sklearn):
    def __init__(self):
        Sklearn.__init__(self)

    def training(self, arr: np.ndarray, indexs, kernel='linear', c=1.0, **kwargs):
        self.model = svm.SVC(kernel=kernel, C=c, probability=True, **kwargs)
        self.model.fit(arr, indexs)

    # 获取支持向量
    def getSupportps(self):
        return self.model.support_vectors_

    # 获取每个类别的支持向量数量
    def getSupportpnum(self):
        return self.model.n_support_


