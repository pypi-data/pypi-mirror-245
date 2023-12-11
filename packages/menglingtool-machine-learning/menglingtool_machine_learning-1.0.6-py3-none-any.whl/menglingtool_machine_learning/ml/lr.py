import sklearn.linear_model as linear
from .__super__ import Sklearn, np


class LinearRegression(Sklearn):
    def __init__(self):
        Sklearn.__init__(self)

    def training(self, xs, ys, **kwargs):
        self.model = linear.LinearRegression(**kwargs)
        xs = xs if xs is not None else range(len(ys))
        if type(ys) is not np.ndarray: ys = np.array(ys)
        if type(xs) is not np.ndarray: xs = np.array(xs)
        self.model.fit(xs.reshape(-1, 1), ys.reshape(-1, 1))

    # 获取支持向量
    def getArgs(self):
        # 回归系数
        a = self.model.coef_
        # 截距
        b = self.model.intercept_
        return a, b

    # 预测
    def predicts(self, xs):
        if type(xs) is not np.ndarray:  xs = np.array(xs)
        pys = self.model.predict(xs.reshape(-1, 1))
        return pys

    # 综合预测
    def predict_all_ys(self, ys, xs=None) -> float:
        xs = xs if xs is not None else range(len(ys))
        if type(ys) is not np.ndarray: ys = np.array(ys)
        if type(xs) is not np.ndarray: xs = np.array(xs)

        v = self.model.score(xs.reshape(-1, 1), ys.reshape(-1, 1))
        return v
