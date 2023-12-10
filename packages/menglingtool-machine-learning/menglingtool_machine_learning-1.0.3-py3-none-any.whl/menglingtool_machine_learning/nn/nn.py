import torch
from torch import nn
from math import floor


class NNer:
    def __init__(self, ceils, if_cuda=True):
        self._device = torch.device("cuda:0" if if_cuda and torch.cuda.is_available() else "cpu")
        self.model = nn.Sequential(*ceils).to(self._device)
        print('NNer_device:', self._device)

    def train(self, X, Y, learn_step=1e-2, min_loss=5e-5, max_train_num=1_0000, loss_print=True):
        X, Y = torch.FloatTensor(X).to(self._device), torch.FloatTensor(Y).to(self._device)
        # 进入训练状态
        self.model.train()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=learn_step)
        loss_fn = nn.MSELoss()
        i = 0
        while True:
            Y0 = self.model(X)
            # 更新参数
            loss = loss_fn(Y0, Y)
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
