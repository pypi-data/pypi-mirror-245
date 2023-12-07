import numpy as np

import torch
import torch.nn as nn

from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import KDTree


class BaseGAN:
    """
    BaseGenerator class provides the base of all GANs.

    All GANs derive from BaseGenerator and inherit its methods and properties
    """

    def __init__(self, discriminator, generator, adaptive, random_state):
        self.dim_ = 0
        self.n_classes_ = 0
        self.device_ = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.random_state_ = random_state

        self.gen_samples_ratio_ = None
        self.x_train_per_class_ = None
        self.column_info_ = []

        # Sets/unsets adaptive training
        self.adaptive_ = adaptive

        # Class encoder
        self.class_encoder_ = OneHotEncoder()

        # Optional classification model for evaluating the effectiveness of this GAN
        self.test_classifier_ = None

        # Discriminator parameters (object, architecture, optimizer)
        self.D_ = None
        self.D_Arch_ = discriminator
        self.D_optimizer_ = None

        # Generator parameters (object, architecture, optimizer)
        self.G_ = None
        self.G_Arch_ = generator
        self.G_optimizer_ = None

    def display(self):
        self.D_.display()
        self.G_.display()

    def get_column_info(self, x_train):
        for c in range(self.dim_):
            col = x_train[:, c:c + 1]
            self.column_info_.append({'max_val': np.max(col), 'min_val': np.min(col)})

    def prepare(self, x_train, y_train):
        """
        Data preparation function. Several auxiliary structures are built here (e.g. samples-per-class tensors, etc.) .

        :param x_train: The training data instances.
        :param y_train: The classes of the training data instances.
        """
        y_train = self.class_encoder_.fit_transform(y_train.reshape(-1, 1)).toarray()

        train_data = np.concatenate((x_train, y_train), axis=1)
        training_data = torch.from_numpy(train_data).to(torch.float32)

        self.dim_ = x_train.shape[1]
        self.n_classes_ = y_train.shape[1]

        # Determine how to sample the conditional GAN in smart training
        self.gen_samples_ratio_ = [int(sum(y_train[:, c])) for c in range(self.n_classes_)]
        # gen_samples_ratio.reverse()

        # Class specific training data for smart training (KL/JS divergence)
        self.x_train_per_class_ = []
        for y in range(self.n_classes_):
            x_class_data = np.array([x_train[r, :] for r in range(y_train.shape[0]) if y_train[r, y] == 1])
            x_class_data = torch.from_numpy(x_class_data).to(torch.float32).to(self.device_)

            self.x_train_per_class_.append(x_class_data)

        self.get_column_info(x_train)

        return training_data

    def select_prepare(self, x_train, y_train, method='knn', k=5, r=0.5):
        """
        Refine the training set with sample filtering.

        :param x_train: The training data instances.
        :param y_train: The classes of the training data instances.
        :param method: 'knn': k-nearest neighbors / 'rad': neighbors inside a surrounding hypersphere.
        :param k: The number of nearest neighbors to retrieve; applied when `method='knn'`.
        :param r: The radius of the hypersphere that includes the neighboring samples; applied when `method='rad'`.
        """
        num_samples = x_train.shape[0]

        # Array with the point labels.
        pts_types = ['NotSet'] * num_samples
        x_sample, y_sample = [], []

        # Build an auxiliary KD-Tree accelerate spatial queries.
        kd_tree = KDTree(x_train, metric='euclidean', leaf_size=40)

        # Nearest-Neighbors method.
        if method == 'knn':
            # Query the KD-Tree to find the nearest neighbors. indices contains the indices of the nearest neighbors
            # in the original dataset -> a row indices[r] contains the 5 nearest neighbors of x_train[r].
            _, indices = kd_tree.query(x_train, k=k)

        elif method == 'rad':
            # Query the KD-Tree to find the neighbors-within-hypersphere of radius=radius. indices contains the indices
            # of the neighbors-within-hypersphere in the original dataset -> a row indices[r] contains the
            # neighbors-within-hypersphere of x_train[r].
            indices = kd_tree.query_radius(x_train, r=r)

        else:
            print("method should be 'knn' or 'rad'; returning the input dataset")
            return self.prepare(x_train, y_train)

        # For each sample in the dataset
        for m in range(num_samples):
            pts_with_same_class = 0

            # Examine its nearest neighbors and assign a label: core/border/outlier/isolated
            num_neighbors = len(indices[m])
            for k in range(num_neighbors):
                nn_idx = indices[m][k]
                if y_train[nn_idx] == y_train[m]:
                    pts_with_same_class += 1

            if num_neighbors == 1:
                pts_types[m] = 'Isolated'
            else:
                t_high = 1.0 * num_neighbors
                t_low = 0.2 * num_neighbors

                if pts_with_same_class >= t_high:
                    pts_types[m] = 'Core'
                    # x_sample.append(x_train[m])
                    # y_sample.append(y_train[m])
                elif t_high > pts_with_same_class > t_low:
                    pts_types[m] = 'Border'
                    x_sample.append(x_train[m])
                    y_sample.append(y_train[m])
                else:
                    pts_types[m] = 'Outlier'

            # print("Sample", m, ":", pts_types[m], "- Neighbors indices:", indices[m], "- Neighbors classes:",
            #      [y_train[indices[m][k]] for k in range(num_neighbors)])

        x_train = np.array(x_sample)
        y_train = np.array(y_sample)

        return self.prepare(x_train, y_train)

    # Use GAN's Generator to create artificial samples i) either from a specific class, ii) or from a random class.
    def sample(self, num_samples, y=None):
        """
        Create artificial samples using the GAN's Generator.

        :param num_samples: The number of samples to generate.
        :param y: The class of the generated samples. If `None`, then samples with random classes are generated.
        """
        if y is None:
            latent_classes = torch.from_numpy(np.random.randint(0, self.n_classes_, num_samples)).to(torch.int64)
            latent_y = nn.functional.one_hot(latent_classes, num_classes=self.n_classes_).to(self.device_)
        else:
            latent_y = nn.functional.one_hot(torch.full(size=(num_samples,), fill_value=y), num_classes=self.n_classes_)

        latent_x = torch.randn((num_samples, self.dim_))

        # concatenate, copy to device, and pass to generator
        latent_data = torch.cat((latent_x, latent_y), dim=1).to(self.device_)

        # Generate data from the model's Generator - The feature values of the generated samples fall into the range:
        # [-1,1]: if the activation function of the output layer of the Generator is nn.Tanh().
        # [0,1]: if the activation function of the output layer of the Generator is nn.Sigmoid().
        generated_samples = self.G_(latent_data)

        # ... so we must reconstruct the samples by scaling them back to their original scale.
        reconstructed_samples = torch.tensor([]).to(self.device_)
        for c in range(self.dim_):
            max_val = self.column_info_[c]['max_val']
            min_val = self.column_info_[c]['min_val']
            # print("=== COL:", c, "\n\t= Info:", self.column_info_[c], "\n\t= Data:\n", generated_samples[:, c:c+1])

            col = generated_samples[:, c:c+1] * ((max_val - min_val) / 2) + (max_val + min_val) / 2

            reconstructed_samples = torch.cat((reconstructed_samples, col), dim=1)
            # print("\n\n\t==== Reconstructed Samples:", reconstructed_samples.shape, "\n", reconstructed_samples)

        return reconstructed_samples
