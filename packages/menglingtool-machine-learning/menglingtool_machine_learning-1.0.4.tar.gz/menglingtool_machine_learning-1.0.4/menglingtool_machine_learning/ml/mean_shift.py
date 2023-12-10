import sklearn.cluster as sc
from .__super__ import Sklearn,np


# https://scikit-learn.org.cn/view/389.html
class MeanShift(Sklearn):
    # n_samples:样本数量
    def __init__(self):
        Sklearn.__init__(self)

    # 设置参数计算相关模型
    # n_samples:要使用的样本数。如果没有提供，则使用所有样本。
    def training(self, arr: np.ndarray, n_samples=None, quantile=0.2):
        # 量化带宽 quantile 量化宽度
        bw = sc.estimate_bandwidth(arr, n_samples=n_samples, quantile=quantile)
        # 均值漂移算法
        self.model = sc.MeanShift(bandwidth=bw, bin_seeding=True)
        # 执行聚类
        self.model.fit(arr)

    # 获取分类后的中心点
    def getAllCenters(self):
        return self.model.cluster_centers_

    # 获取分类后的类型标签
    def getAllLabels(self):
        return self.model.labels_

    # 预测
    def predicts(self, arr: np.ndarray, ifit=False):
        assert len(arr.shape) == 2
        if ifit:
            # 聚类影响源模型
            results = self.model.fit_predict(arr)
        else:
            # 不影响原模型预测
            results = self.model.predict(arr)
        return results

    # 综合预测
    def predict_all(self, arr: np.ndarray, indexs) -> float:
        assert arr.shape[0] == len(indexs)
        parr = self.model.predict(arr)
        n = 0
        for p, index in zip(parr, indexs):
            if p == index: n += 1
        return n / len(indexs)

