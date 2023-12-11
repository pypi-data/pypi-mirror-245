from math import prod
import torch
from torch import nn

'''
nn.MSELoss
均方误差（Mean Squared Error，MSE）：常用于回归问题，衡量预测值与真实值之间的平方差。适用于输出是连续值的情况，如房价预测、股票价格预测等。

nn.CrossEntropyLoss
交叉熵损失函数（Cross Entropy Loss）：常用于分类问题，特别是多分类问题。适用于输出是概率分布的情况，如图像分类、文本分类等。

nn.BCELoss（二分类） nn.BCEWithLogitsLoss（多分类）
对数损失函数（Log Loss）：也常用于分类问题，特别是二分类问题。适用于输出是概率分布的情况，如广告点击率预测、风险预测等。

nn.HingeEmbeddingLoss
Hinge损失函数：常用于支持向量机（SVM）中，适用于分类问题，特别是支持向量机的线性分类器。

nn.SmoothL1Loss
Huber损失函数：是一种对异常值比较鲁棒的损失函数，介于均方误差和绝对误差之间，适用于回归问题，对异常值比较敏感的情况。
'''


class _TF(nn.Module):
    def forward(self, X):
        return X.reshape(-1, prod(X.size()[1:]))


class NNer:
    def __init__(self, if_cuda=True, optim_fn=None, loss_fner=None):
        self._device = torch.device("cuda:0" if if_cuda and torch.cuda.is_available() else "cpu")
        self.model = nn.Sequential(*self.getLayers()).to(self._device)
        # 优化器函数
        self.optim_fn = optim_fn or torch.optim.Adam
        # 损失函数
        self.loss_fn = loss_fner or nn.CrossEntropyLoss()
        print('NNer_device:', self._device)

    # 重写方法
    def getLayers(self) -> list:
        raise ValueError('需重写方法-forward')

    # 获取一维输入
    def getOneDimLayer(self):
        return _TF()

    def train(self, X, Y, learn_step=1e-3, min_loss=1e-2, max_train_num=5_000, loss_print=True,
              ):
        X, Y = torch.FloatTensor(X).to(self._device), torch.FloatTensor(Y).to(self._device)
        # 进入训练状态
        self.model.train()
        optimizer = self.optim_fn(self.model.parameters(), lr=learn_step)
        i = 0
        while True:
            Y0 = self.model(X)
            # 更新参数
            loss = self.loss_fn(Y0, Y)
            # loss.requires_grad_(True)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if loss_print and i % 10 == 0: print(f'loss-{i}: {loss.item()}')
            i += 1
            if i >= max_train_num or loss <= min_loss: break

    def predict(self, X, return_index=True):
        X = torch.FloatTensor(X).to(self._device)
        # 进入验证状态
        self.model.eval()
        # 仅验证不更新模型
        with torch.no_grad():
            # 转换为Tensor
            Y = self.model(X)
            if return_index:
                return [y.argmax().item() for y in Y]
            else:
                return Y

    def saveModel(self, filepath):
        torch.save(self.model.state_dict(), filepath)

    def loadModel(self, filepath):
        self.model.load_state_dict(torch.load(filepath))
