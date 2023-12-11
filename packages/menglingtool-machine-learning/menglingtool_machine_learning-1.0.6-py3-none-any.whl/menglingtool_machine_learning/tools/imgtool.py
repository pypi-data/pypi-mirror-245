from PIL import Image
import numpy as np


# 等比例缩放并填充
def getImgArr(imgpath, size: tuple):
    try:
        img = Image.open(imgpath).convert("RGB")
        img.thumbnail(size)
        arr = np.zeros((*size, 3))
        # 图片weigth及high
        arr[:img.size[1], :img.size[0], :] = np.array(img)
        # 将通道维度移至首位
        arr = np.moveaxis(arr, -1, 0)
        assert arr.shape == (3, *size)
        return arr
    except:
        print('错误', imgpath)
        return None


def getXY(imgpaths, ys, size: tuple):
    X, Y = [], []
    for i, imgpath in enumerate(imgpaths):
        arr = getImgArr(imgpath, size)
        if arr is not None and len(arr) > 0:
            X.append(arr)
            Y.append(ys[i])
    return np.stack(X), np.array(Y)
