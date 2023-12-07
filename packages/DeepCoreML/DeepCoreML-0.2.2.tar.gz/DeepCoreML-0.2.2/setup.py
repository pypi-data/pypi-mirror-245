from distutils.core import setup
from setuptools import find_packages

DESCRIPTION = 'A collection of Machine Learning techniques for data management and augmentation.'
LONG_DESCRIPTION = '<p>DeepCoreML is a collection of Machine Learning techniques for data management, engineering, ' \
    'and augmentation. More specifically, DeepCoreML includes modules for:</p>'\
    '<ul>' \
    '<li>Dataset management</li>' \
    '<li>Text data preprocessing</li>' \
    '<li>Text representation, vectorization, embeddings</li>' \
    '<li>Dimensionality Reduction</li>' \
    '<li>Generative Modeling</li>' \
    '<li>Imbalanced Datasets</li>' \
    '</ul>' \
    '<p>Licence:</p> Apache License, 2.0 (Apache-2.0)' \
    '<p><b>Dependencies:</b> scikit-learn, imbalanced-learn, pytorch, numpy, pandas.</p>'\
    '<p><b>GitHub repository:</b> '\
    '<a href="https://github.com/lakritidis/DeepCoreML">https://github.com/lakritidis/DeepCoreML</a></p>' \
    '<p><b>Publications:</b><ul>' \
    '<li>L. Akritidis, A. Fevgas, M. Alamaniotis, P. Bozanis, "Conditional Data Synthesis with Deep Generative Models '\
    'for Imbalanced Dataset Oversampling", In Proceedings of the 35th IEEE International Conference on Tools with '\
    'Artificial Intelligence (ICTAI), to appear, 2023.</li>' \
    '<li>L. Akritidis, P. Bozanis, "A Multi-Dimensional Survey on Learning from Imbalanced Data", Chapter in Machine '\
    'Learning Paradigms - Advances in Theory and Applications of Learning from Imbalanced Data, to appear, 2023.</li>' \
    '<li>L. Akritidis, P. Bozanis, "<a href="https://link.springer.com/article/10.1007/s42979-023-01913-y">' \
    'Low Dimensional Text Representations for Sentiment Analysis NLP Tasks</a>", Springer Nature (SN) Computer '\
    'Science, vol. 4, no. 5, 474, 2023.</li>' \
    '</ul></p>'

setup(
    name='DeepCoreML',
    version='0.2.2',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author="Leonidas Akritidis",
    author_email="lakritidis@ihu.gr",
    maintainer="Leonidas Akritidis",
    maintainer_email="lakritidis@ihu.gr",
    packages=find_packages(),
    package_data={'': ['GANs/*']},
    url='https://github.com/lakritidis/DeepCoreML',
    install_requires=["numpy", "pandas", "nltk", "matplotlib", "seaborn", "gensim", "bs4",
                      "torch>=2.0.0+cu117",
                      "transformers>=4.28.1",
                      "scikit-learn>=1.0.0",
                      "imblearn>=0.0"],
    license="Apache",
    keywords=[
        "data engineering", "data management", "text vectorization", "text processing", "dimensionality reduction",
        "imbalanced data", "machine learning", "deep learning"]
)
