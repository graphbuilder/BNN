import torch.nn as nn
import torch
from torchsummary import summary
from .binarized_modules import  BinarizeConv2d

class MCNET(nn.Module):
    def __init__(self):
        super(MCNET, self).__init__()

        self.features2 = nn.Sequential(
            BinarizeConv2d(3, 16, kernel_size=3, padding=0, bias=False),  # 5
            nn.Hardtanh(inplace=True),
        )

        self.features3 = nn.Sequential(
            BinarizeConv2d(16, 23, kernel_size=3, padding=0, bias=False),  # 3
            nn.Hardtanh(inplace=True),
        )

        self.features4 = nn.Sequential(
            BinarizeConv2d(23, 2, kernel_size=3, padding=0, bias=False),  # 3->1
            nn.Hardtanh(inplace=True),
        )


    def forward(self, inputs):

        x = self.features2(inputs)
        x = self.features3(x)
        x = self.features4(x)
        x = x.view(x.size(0), -1)

        return x

if __name__ == "__main__":
    img = torch.rand((1, 3, 56, 56), dtype = torch.float)
    net = MCNET()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = net.to(device)
    summary(model, (3, 56, 56))
    