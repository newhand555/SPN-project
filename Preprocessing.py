from torchvision.datasets import MNIST
from torch.utils.data import DataLoader, Subset
import torchvision.transforms as tfs
import numpy as np
import torch
import os

co_table = [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0],
                [0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 1]]

_GRAYSCALE_THRESHOLD = 0.5
_IMAGE_SIZE = 28
_DATA_SIZE = 10000

torch.set_printoptions(threshold=100000)
data_path = os.getcwd().join('/mnist')
data_set = MNIST(data_path,  train=True, transform=tfs.Compose([tfs.ToTensor()]), download=True)
target_dl = DataLoader(data_set, batch_size=64, shuffle=True)


def get_data_loader(path=os.getcwd().join('/mnist')):
    data_set = MNIST(path, train=True, transform=tfs.Compose([tfs.ToTensor()]), download=True)
    data_set = Subset(data_set, indices=list(range(_DATA_SIZE)))
    return DataLoader(data_set, batch_size=64, shuffle=True, drop_last=True)


# Stupid transformer s.t. convert integer to 4-bit binary
def stupid_tfs(input_tensor):
    res = []
    global co_table

    for val in input_tensor:
        res.append(co_table[val])

    return torch.from_numpy(np.asarray(res, dtype=int))


def generate_data(feature, label):
    feature = (feature >= _GRAYSCALE_THRESHOLD).long().reshape(-1, _IMAGE_SIZE ** 2)
    label = stupid_tfs(label).reshape(-1, 4)
    res = torch.cat((feature, label), 1).numpy().T

    return res


for f, l in target_dl:
    f = (f >= _GRAYSCALE_THRESHOLD).long().reshape(-1, _IMAGE_SIZE ** 2)
    l = stupid_tfs(l).reshape(-1, 4)
    test = torch.cat((f, l), 1).numpy().T