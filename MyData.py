import os
import random
import numpy as np
import torch.utils.data as data
import torchvision.transforms as transforms

from PIL import Image

class MyData(data.Dataset):
    def __init__(self, txt_path, transform=None, target_transform = None):
        fh = open(txt_path, 'r')
        imgs = []
        for line in fh:
            line = line.rstrip()
            words = line.split()
            imgs.append((words[0], int(words[1])))
            self.imgs = imgs
            self.transform = transform
            self.target_transform = target_transform

    def __getitem__(self, index):
        fn, label = self.imgs[index]
        # print(fn)
        # print(label)
        img = Image.open(fn).convert('RGB')
        if self.transform is not None:
            img = self.transform(img)
        return img, label
    
    def __len__(self):
        return len(self.imgs)


if __name__ == "__main__":
    pass



