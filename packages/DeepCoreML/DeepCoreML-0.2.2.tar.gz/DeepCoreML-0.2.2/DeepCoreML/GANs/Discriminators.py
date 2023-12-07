import torch.nn as nn


class Discriminator(nn.Module):
    """
    A typical GAN discriminator is a binary classifier that outputs 0/1 (real/fake) values. It identifies fake samples
    (coming from Generator) from real samples (coming from the dataset). As its performance improves during training,
    the Generator's performance also improves.
    """
    def __init__(self, architecture=(128, 128), input_dim=2, p=0.3, negative_slope=0.01):
        """
        This Discriminator is implemented as a typical feed-forward fully-connected network. As a binary classifier, it
        includes only one neuron in the output layer; its activation is the Logistic function. Regarding all the other
        dense layers, Leaky ReLU is the activation function of all neurons. Each dense layer is followed by a Dropout
        layer that prevents the model from over-fitting.

        :param architecture: The architecture of the fully connected net; a tuple with the number of neurons per layer.
        :param input_dim: The dimensionality of the input (i.e. training) data.
        :param p: The probability that a weight is dropped at each training epoch - Passed to the Dropout layer.
        :param negative_slope: Controls the angle of the negative slope (used for negative inputs) - Passed to LeakyReLU
        """
        super().__init__()

        seq = []
        dim = input_dim

        # The hidden layers:
        for features in architecture:
            seq += [nn.Linear(in_features=dim, out_features=features),
                    nn.Dropout(p=p),
                    nn.LeakyReLU(negative_slope=negative_slope)]

            dim = features

        # The output layer:
        seq += [nn.Linear(in_features=dim, out_features=1),
                nn.Sigmoid()]

        self.model = nn.Sequential(*seq)

    def forward(self, x):
        return self.model(x)

    def display(self):
        print(self.model)
        print(self.model.parameters())


class PackedDiscriminator(nn.Module):
    """
    A typical GAN discriminator is a binary classifier that outputs 0/1 (real/fake) values. It identifies fake samples
    (coming from Generator) from real samples (coming from the dataset). As its performance improves during training,
    the Generator's performance also improves.

    A packed Discriminator accepts multiple inputs at once in the form of concatenated vectors. It has been proved that
    feeding the Discriminator with multiple input vectors with the same label limits the problem of mode collapse. The
    Generator architecture remains the same.
    """

    def __init__(self, architecture=(128, 128), input_dim=2, pac=10, p=0.3, negative_slope=0.01):
        """
        This Discriminator is implemented as a typical feed-forward fully-connected network. As a binary classifier, it
        includes only one neuron in the output layer; its activation is the Logistic function. Regarding all the other
        dense layers, Leaky ReLU is the activation function of all neurons. Each dense layer is followed by a Dropout
        layer that prevents the model from over-fitting.

        A packed Discriminator is implemented on the basis of the original Discriminator, but we also pass a pac
        argument and the input dimensionality. The number of neurons in the input layer is `pac * input_dim`.

        :param architecture: The architecture of the fully connected net; a tuple with the number of neurons per layer.
        :param input_dim: The dimensionality of the input (i.e. training) data.
        :param p: The probability that a weight is dropped at each training epoch - Passed to the Dropout layer.
        :param negative_slope: Controls the angle of the negative slope (used for negative inputs) - Passed to LeakyReLU
        """
        super().__init__()

        seq = []
        dim = pac * input_dim
        for lay in architecture:
            seq += [nn.Linear(dim, lay),
                    nn.Dropout(p=p),
                    nn.LeakyReLU(negative_slope=negative_slope)]
            dim = lay

        seq += [nn.Linear(dim, 1),
                nn.Sigmoid()]
        self.model = nn.Sequential(*seq)

    def forward(self, x):
        return self.model(x)

    def display(self):
        print(self.model)
        print(self.model.parameters())
