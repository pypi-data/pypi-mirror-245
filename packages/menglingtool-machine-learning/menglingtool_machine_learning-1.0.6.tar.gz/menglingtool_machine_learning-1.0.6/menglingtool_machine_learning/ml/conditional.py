from sklearn.naive_bayes import GaussianNB
from .__super__ import Sklearn,np


# 高斯朴素贝叶斯
# 适合变量参数较少的分类情况
class Conditional(Sklearn):
    def __init__(self):
        Sklearn.__init__(self)

    def training(self, arr: np.ndarray, indexs, var_smoothing=1e-09):
        self.model = GaussianNB(var_smoothing=var_smoothing)
        self.model.fit(arr, indexs)
