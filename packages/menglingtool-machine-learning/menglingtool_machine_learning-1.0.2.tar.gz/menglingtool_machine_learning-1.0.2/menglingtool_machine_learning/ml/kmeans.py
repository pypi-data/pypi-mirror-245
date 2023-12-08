from sklearn.cluster import KMeans
from .__super__ import Sklearn,np


class Kmeans(Sklearn):
    def __init__(self):
        Sklearn.__init__(self)

    # 设置参数计算相关模型
    def training(self, arr: np.ndarray, center_num, random_state=None, **kwargs):
        self.model = KMeans(n_clusters=center_num, random_state=random_state, **kwargs)
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


