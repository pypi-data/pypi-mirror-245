import torch.nn as nn


class Generator(nn.Module):
    """
    The Generator is the part of the GAN that ultimately produces artificial data.
    """
    def __init__(self, architecture=(128, 128), input_dim=2, output_dim=2, normalize=False, negative_slope=0.01):
        """
        This Generator is a feed-forward fully connected network implemented with a stack of residual blocks.
        Leaky ReLU is the activation function of all neurons in each dense layer. Dropout is not applied here.

        :param architecture: The architecture of the fully connected net; a tuple with the number of neurons per layer.
        :param input_dim: The dimensionality of the input (i.e. training) data.
        :param output_dim: The dimensionality of the data that will be generated; in most cases, equal to `input_dim`.
        :param normalize: If True, appends a 1-D Batch Normalization layer after each dense layer. NOT recommended!!
        :param negative_slope: Controls the angle of the negative slope (used for negative inputs) - Passed to LeakyReLU
        """
        super().__init__()

        def residual_block(in_dim, out_dim, norm, slope):
            layers = [nn.Linear(in_features=in_dim, out_features=out_dim)]

            if norm:
                layers.append(nn.BatchNorm1d(out_dim))

            layers.append(nn.LeakyReLU(negative_slope=slope))

            return layers

        seq = []
        dim = input_dim
        for features in architecture:
            seq += [*residual_block(dim, features, normalize, negative_slope)]
            dim = features

        seq += [nn.Linear(dim, output_dim),
                nn.Tanh()]
        self.model = nn.Sequential(*seq)

    def forward(self, x):
        return self.model(x)

    def display(self):
        print(self.model)
        print(self.model.parameters())
