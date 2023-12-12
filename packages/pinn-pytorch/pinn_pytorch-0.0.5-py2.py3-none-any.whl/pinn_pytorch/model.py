import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, input_size, layer_size, output_size):
        super(MLP, self).__init__()
        layers = []
        layers.append(nn.Linear(input_size, layer_size[0]))
        for i in range(1, len(layer_size)):
            layers.append(nn.Linear(layer_size[i-1], layer_size[i]))
            layers.append(nn.Tanh())
        layers.append(nn.Linear(layer_size[i], output_size))
        self.layers = nn.Sequential(*layers)
        
    def forward(self, x):
        return self.layers(x)
