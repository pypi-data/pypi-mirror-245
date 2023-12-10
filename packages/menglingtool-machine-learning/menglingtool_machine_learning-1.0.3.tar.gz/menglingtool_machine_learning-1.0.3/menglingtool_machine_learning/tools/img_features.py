import numpy as np
import tensorflow as tf
import cv2


# 将图片处理为0-1的单列数组
def _getImages(picpaths: list, size: tuple, strict: bool = True) -> (list, np.ndarray):
    pics, images = [], []
    for pic in picpaths:
        if strict:
            img = cv2.resize(cv2.imread(pic), size)
        else:
            try:
                img = cv2.resize(cv2.imread(pic), size)
            except:
                print(f'图片处理错误，可能为路径存在中文情况：{pic}')
                continue
        pics.append(pic)
        images.append(img)
    assert images
    images = np.array(np.float32(images).reshape(len(images), -1) / 255)
    return pics, images


# 特征提取
def getFeatures(picpaths, size: tuple, strict=True, pipeline=3) -> (list, np.ndarray):
    picpaths, images = _getImages(picpaths, size, strict=strict)
    input_shape = (*size, pipeline)
    model = tf.keras.applications.MobileNetV2(include_top=False,
                                              weights='imagenet',
                                              input_shape=input_shape)
    predictions = model.predict(images.reshape(-1, *input_shape))
    pred_images = predictions.reshape(images.shape[0], -1)
    return picpaths, pred_images
