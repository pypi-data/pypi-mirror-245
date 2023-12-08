import torch
from torch import nn
from math import floor


class NNer:
    def __init__(self, ceils):
        self.model = nn.Sequential(*ceils)

    def train(self, X, Y, learn_step=1e-2, train_num=100, loss_print=False):
        X, Y = torch.FloatTensor(X), torch.FloatTensor(Y)
        # 进入训练状态
        self.model.train()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=learn_step)
        loss_fn = nn.MSELoss()
        for i in range(train_num):
            Y0 = self.model(X)
            # 更新参数
            loss = loss_fn(Y0, Y)
            # loss.requires_grad_(True)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if loss_print and i % 10 == 0: print('loss:', loss.item())

    def predict(self, X, return_index=True):
        X = torch.FloatTensor(X)
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