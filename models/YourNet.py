from torch import nn
import torch.nn.functional as F

class YourNet(nn.Module):
    ###################### Begin #########################
    # You can create your own network here or copy our reference model (LeNet5)
    # We will conduct a unified test on this network to calculate your score

    def __init__(self):
        super(YourNet, self).__init__()

    def forward(self, x):
        pass

    ######################  End  #########################