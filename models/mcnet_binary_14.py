import torch.nn as nn
import torch
from torchsummary import summary
from .binarized_modules import  BinarizeConv2d

class MCNET(nn.Module):
    def __init__(self):
        super(MCNET, self).__init__()

        self.p0 = nn.Sequential(
            nn.ConstantPad2d(1, value=1),
        )

        self.features1 = nn.Sequential(
            # nn.ConstantPad2d(1, value=1),                               
            BinarizeConv2d(3, 8, kernel_size=3, padding=0, bias=False),  # 14
            nn.Hardtanh(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 7
        )

        self.features2 = nn.Sequential(
            BinarizeConv2d(8, 16, kernel_size=3, padding=0, bias=False),  # 5
            nn.Hardtanh(inplace=True),
        )

        self.features3 = nn.Sequential(
            BinarizeConv2d(16, 32, kernel_size=3, padding=0, bias=False),  # 3
            nn.Hardtanh(inplace=True),
        )

        self.features4 = nn.Sequential(
            BinarizeConv2d(32, 2, kernel_size=3, padding=0, bias=False),  # 3->1
            nn.Hardtanh(inplace=True),
        )

    def forward(self, inputs):
        x = self.p0(inputs)
        x = self.features1(x)
        x = self.features2(x)
        x = self.features3(x)
        x = self.features4(x)
        x = x.view(x.size(0), -1)

        return x

    