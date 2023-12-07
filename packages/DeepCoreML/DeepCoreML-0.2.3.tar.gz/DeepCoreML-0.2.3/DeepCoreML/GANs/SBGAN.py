# Conditional GAN Implementation
import numpy as np
import torch
import torch.nn as nn

from torch.utils.data import DataLoader

from sklearn.metrics import accuracy_score

from .BaseGenerators import BaseGAN
from .Discriminators import PackedDiscriminator
from .Generators import Generator


class sbGAN(BaseGAN):
    """
    Conditional GANs (cGANs) conditionally generate data from a specific class. In contrast to typical GANs, cGANs are
    trained by providing both the Generator and the Discriminator not only with the feature vectors but also with the
    respective class labels.

    In a typical cGAN implementation, the class labels are one-hot-encoded vectors. They are concatenated with the input
    vectors and fed to both the Discriminator and the Generator.
    """

    def __init__(self, discriminator=(128, 128), generator=(256, 256), pac=10, adaptive=False,
                 method='knn', k=5, r=10, random_state=0):
        """
        Initializes a Conditional GAN.

        :param discriminator: Discriminator architecture (number of neurons in each dense layer).
        :param generator: Generator architecture (number of neurons in each dense layer).
        :param pac: The number of input samples to be concatenated and fed as input in the Discriminator.
        :param adaptive: Sets/Unsets adaptive training.
        :param method: 'knn': k-nearest neighbors / 'rad': neighbors inside a surrounding hypersphere.
        :param k: The number of nearest neighbors to retrieve; applied when `method='knn'`.
        :param r: The radius of the hypersphere that includes the neighboring samples; applied when `method='rad'`.

        """
        super().__init__(discriminator, generator, adaptive, random_state)

        self.pac_ = pac
        self.method_ = method
        self.n_neighbors_ = k
        self.radius_ = r

    def train_batch(self, real_data, loss_function):
        """
        Given a batch of input data, `train_batch` updates the Discriminator and Generator weights using the respective
        optimizers and back propagation.

        :param real_data: data for cGAN training: a batch of concatenated sample vectors + one-hot-encoded class vectors
        :param loss_function: the loss function for cGAN training - applied to both the Discriminator and Generator.
        """

        # If the size of the batch does not allow an organization of the input vectors in packs of size self.pac_, then
        # abort silently and return without updating the model parameters.
        num_samples = real_data.shape[0]
        if num_samples % self.pac_ != 0:
            return 0, 0

        packed_samples = num_samples // self.pac_

        # DISCRIMINATOR TRAINING
        # Create fake samples from Generator
        self.D_.zero_grad()

        # 1. Randomly take samples from a normal distribution
        # 2. Assign one-hot-encoded random classes
        # 3. Pass the fake data (samples + classes) to the Generator
        latent_x = torch.randn((num_samples, self.dim_))
        latent_classes = torch.from_numpy(np.random.randint(0, self.n_classes_, num_samples)).to(torch.int64)
        latent_y = nn.functional.one_hot(latent_classes, num_classes=self.n_classes_)
        latent_data = torch.cat((latent_x, latent_y), dim=1)

        # 4. The Generator produces fake samples (their labels are 0)
        fake_x = self.G_(latent_data.to(self.device_))
        fake_labels = torch.zeros((packed_samples, 1))

        # 5. The real samples (coming from the dataset) with their one-hot-encoded classes are assigned labels eq. to 1.
        real_x = real_data[:, 0:self.dim_]
        real_y = real_data[:, self.dim_:(self.dim_ + self.n_classes_)]
        real_labels = torch.ones((packed_samples, 1))
        # print(real_x.shape, real_y.shape)

        # 6. Mix (concatenate) the fake samples (from Generator) with the real ones (from the dataset).
        all_x = torch.cat((real_x.to(self.device_), fake_x))
        all_y = torch.cat((real_y, latent_y)).to(self.device_)
        all_labels = torch.cat((real_labels, fake_labels)).to(self.device_)
        all_data = torch.cat((all_x, all_y), dim=1)

        # 7. Reshape the data to feed it to Discriminator (num_samples, dimensionality) -> (-1, pac * dimensionality)
        # The samples are packed according to self.pac parameter.
        all_data = all_data.reshape((-1, self.pac_ * (self.dim_ + self.n_classes_)))

        # 8. Pass the mixed data to the Discriminator and train the Discriminator (update its weights with backprop).
        # The loss function quantifies the Discriminator's ability to classify a real/fake sample as real/fake.
        d_predictions = self.D_(all_data)
        disc_loss = loss_function(d_predictions, all_labels)
        disc_loss.backward()
        self.D_optimizer_.step()

        # GENERATOR TRAINING
        self.G_.zero_grad()

        latent_x = torch.randn((num_samples, self.dim_))
        latent_classes = torch.from_numpy(np.random.randint(0, self.n_classes_, num_samples)).to(torch.int64)
        latent_y = nn.functional.one_hot(latent_classes, num_classes=self.n_classes_)
        latent_data = torch.cat((latent_x, latent_y), dim=1)

        fake_x = self.G_(latent_data.to(self.device_))

        all_data = torch.cat((fake_x, latent_y.to(self.device_)), dim=1)

        # Reshape the data to feed it to Discriminator ( (num_samples, dimensionality) -> ( -1, pac * dimensionality )
        all_data = all_data.reshape((-1, self.pac_ * (self.dim_ + self.n_classes_)))

        d_predictions = self.D_(all_data)

        gen_loss = loss_function(d_predictions, real_labels.to(self.device_))
        gen_loss.backward()
        self.G_optimizer_.step()

        return disc_loss, gen_loss

    def train(self, x_train, y_train, epochs=1000, batch_size=32, lr=0.001, loss_function=nn.BCELoss()):
        """
        Conventional cGAN training. The Generator and the Discriminator are trained simultaneously in the traditional
        adversarial fashion by optimizing `loss_function`.

        :param x_train: The training data instances.
        :param y_train: The classes of the training data instances.
        :param epochs: The maximum number of training epochs.
        :param batch_size: Number of data instances in a training batch.
        :param lr: The learning rate used in the optimizers (same in Discriminator and Generator)
        :param loss_function: The loss function (same in Discriminator and Generator)
        """
        # Modify the size of the batch to align with self.pac_
        factor = batch_size // self.pac_
        batch_size = factor * self.pac_

        # select_prepare: implemented in BaseGenerators.py
        training_data = self.select_prepare(x_train, y_train, method=self.method_, k=self.n_neighbors_, r=self.radius_)

        train_dataloader = DataLoader(training_data, batch_size=batch_size, shuffle=True)

        self.D_ = PackedDiscriminator(self.D_Arch_, input_dim=self.dim_ + self.n_classes_,
                                      pac=self.pac_).to(self.device_)
        self.G_ = Generator(self.G_Arch_, input_dim=self.dim_ + self.n_classes_, output_dim=self.dim_,
                            normalize=True).to(self.device_)

        self.D_optimizer_ = torch.optim.Adam(self.D_.parameters(), lr=lr)
        self.G_optimizer_ = torch.optim.Adam(self.G_.parameters(), lr=lr)

        disc_loss, gen_loss = 0, 0
        for epoch in range(epochs):
            for n, real_data in enumerate(train_dataloader):
                disc_loss, gen_loss = self.train_batch(real_data, loss_function)

                # if epoch % 10 == 0 and n >= num_total_samples // batch_size:
                #    print(f"Epoch: {epoch} Loss D.: {disc_loss} Loss G.: {gen_loss}")

        return disc_loss, gen_loss

    def adaptive_train(self, x_train, y_train, clf, epochs=1000, batch_size=64, lr=0.001, loss_function=nn.BCELoss(),
                       gen_samples_ratio=None):
        """
        Adaptive training by evaluating the quality of generated data during each epoch. Adaptive training is
        self-terminated when max training accuracy (of a classifier `clf`) is achieved.

        :param x_train: The training data instances.
        :param y_train: The classes of the training data instances.
        :param clf: A classifier that has been previously trained on the training set.
        :param epochs: The maximum number of training epochs.
        :param batch_size: Number of data instances in a training batch.
        :param lr: The learning rate used in the optimizers (same in Discriminator and Generator)
        :param loss_function: The loss function (same in Discriminator and Generator)
        :param gen_samples_ratio: A tuple/list that denotes the number of samples to be generated from each class.
        """

        # Use KL Divergence to measure the distance between the real and generated data.
        kl_loss = nn.KLDivLoss(reduction="sum", log_target=True)

        factor = batch_size // self.pac_
        batch_size = factor * self.pac_

        # select_prepare: implemented in BaseGenerators.py
        training_data = self.select_prepare(x_train, y_train, method=self.method_, k=self.n_neighbors_, r=self.radius_)
        train_dataloader = DataLoader(training_data, batch_size=batch_size, shuffle=True)

        self.D_ = PackedDiscriminator(self.D_Arch_, input_dim=self.dim_ + self.n_classes_,
                                      pac=self.pac_).to(self.device_)
        self.G_ = Generator(self.G_Arch_, input_dim=self.dim_ + self.n_classes_, output_dim=self.dim_,
                            normalize=True).to(self.device_)

        self.D_optimizer_ = torch.optim.Adam(self.D_.parameters(), lr=lr)
        self.G_optimizer_ = torch.optim.Adam(self.G_.parameters(), lr=lr)

        if gen_samples_ratio is None:
            gen_samples_ratio = self.gen_samples_ratio_

        generated_data = [[None for _ in range(self.n_classes_)] for _ in range(epochs)]
        mean_met = np.zeros(epochs)
        mean_kld = np.zeros(epochs)

        # Begin training in epochs
        disc_loss, gen_loss = 0, 0
        for epoch in range(epochs):

            # Train the GAN in batches
            for n, real_data in enumerate(train_dataloader):
                disc_loss, gen_loss = self.train_batch(real_data, loss_function)

            # After the GAN has been trained on the entire dataset (for the running epoch), perform sampling with the
            # Generator (of the running epoch)
            sum_acc, sum_kld = 0, 0
            for y in range(self.n_classes_):
                # print("\tSampling Class y:", y, " Gen Samples ratio:", gen_samples_ratio[y])
                generated_data[epoch][y] = self.sample(gen_samples_ratio[y], y)

                # Convert the real data of this batch to a log-probability distribution
                real_x_log_prob = torch.log(nn.Softmax(dim=0)(self.x_train_per_class_[y]))

                # Convert the generated data of this batch to a log-probability distribution
                gen_x_log_prob = torch.log(nn.Softmax(dim=0)(generated_data[epoch][y]))

                # Compute the KL Divergence between the real and generated data
                kld = kl_loss(real_x_log_prob, gen_x_log_prob)

                # Move the generated data to CPU and compute the classifier's performance
                generated_data[epoch][y] = generated_data[epoch][y].cpu().detach().numpy()

                if self.test_classifier_ is not None:
                    y_predicted = clf.predict(generated_data[epoch][y])
                    y_ref = np.empty(y_predicted.shape[0])
                    y_ref.fill(y)

                    acc = accuracy_score(y_ref, y_predicted)
                    sum_acc += acc

                    # print("\t\tModel Accuracy for this class:", acc, " - kl div=", kld)

                sum_kld += kld

                # print(f"Epoch: {epoch+1} \tClass: {y} \t Accuracy: {acc}")

            # if (epoch+1) % 10 == 0:
            mean_met[epoch] = sum_acc / self.n_classes_
            mean_kld[epoch] = sum_kld / self.n_classes_

            print("Epoch %4d \t Loss D.=%5.4f \t Loss G.=%5.4f \t Mean Acc=%5.4f \t Mean KLD=%5.4f" %
                  (epoch + 1, disc_loss, gen_loss, mean_met[epoch], mean_kld[epoch]))

        return generated_data, (mean_met, mean_kld)

    def fit(self, x_train, y_train):
        """
        `fit` invokes the GAN training process. `fit` renders the CGAN class compatible with `imblearn`'s interface,
         allowing its usage in over-sampling/under-sampling pipelines.

        :param x_train: The training data instances.
        :param y_train: The classes of the training data instances.
        """
        self.train(self, x_train, y_train)

    def fit_resample(self, x_train, y_train):
        """
        `fit_transform` invokes the GAN training process. `fit_transform` renders the CGAN class compatible with
        `imblearn`'s interface, allowing its usage in over-sampling/under-sampling pipelines.

        :param x_train: The training data instances.
        :param y_train: The classes of the training data instances.
        """
        self.train(x_train, y_train, epochs=100)
        generated_data = [None for _ in range(self.n_classes_)]

        majority_class = np.array(self.gen_samples_ratio_).argmax()
        num_majority_samples = np.max(np.array(self.gen_samples_ratio_))

        x_over_train = np.copy(x_train)
        y_over_train = np.copy(y_train)

        for cls in range(self.n_classes_):
            if cls != majority_class:
                samples_to_generate = num_majority_samples - self.gen_samples_ratio_[cls]

                # print("\tSampling Class y:", y, " Gen Samples ratio:", gen_samples_ratio[y])
                generated_data[cls] = self.sample(samples_to_generate, cls).cpu().detach()

                min_classes = np.full(samples_to_generate, cls)

                x_over_train = np.vstack((x_over_train, generated_data[cls]))
                y_over_train = np.hstack((y_over_train, min_classes))

        # balanced_data = np.hstack((x_over_train, y_over_train.reshape((-1, 1))))
        # return balanced_data

        return x_over_train, y_over_train
