import numpy as np
from sklearn.datasets import make_blobs, make_regression


# 获取随机分布数据集样本
# https://scikit-learn.org.cn/view/556.html
# n_samples:行数   n_features:特征数(列数) centers:集块数量(标签种类)
def getRandomBlobs(n_samples, n_features, random_state: int = None, center_num=2, **kwargs):
    arr, indexs = make_blobs(n_samples=n_samples, centers=center_num, n_features=n_features,
                             random_state=random_state, **kwargs)
    return arr, indexs


# 获取随机回归数据集样本
# n_informative:信息特征的数量，即用于构建用于生成输出的线性模型的特征的数量  noise:噪音,数据集混乱程度,默认为0不混乱
def getRandomRegression(n_samples, n_features=1, random_state: int = None, n_informative=10, noise=50, **kwargs) \
        -> (np.ndarray, list):
    xarr, indexs = make_regression(n_samples=n_samples, n_features=n_features, noise=noise,
                                   random_state=random_state, n_informative=n_informative, **kwargs)
    return xarr, indexs
