# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import umap.umap_ as ump
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import matplotlib.pyplot as plt
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

from gensim.downloader import load


def outputGraph(df, embedding):
    fig = plt.figure(figsize=(15, 15))
    fig.suptitle(df.title)
    plt.scatter(embedding[:, 0], embedding[:, 1],
                c=df.data[:20000]['class'], cmap="plasma", s=2)


def UMAPAlgorithm(df):
    umap = ump.UMAP(random_state=20)

    embedding = umap.fit_transform(
        df.data[:20000].drop('class', axis=1))
    outputGraph(df, embedding)


def TSNEAlgorithm(df):
    tsne = TSNE(n_components=2, random_state=20)

    embedding = tsne.fit_transform(df.data[:20000].drop('class', axis=1))
    outputGraph(df, embedding)


def PCAAlgorithm(df):
    pca = PCA(n_components=2, random_state=20)

    embedding = pca.fit_transform(df.data[:20000].drop('class', axis=1))
    outputGraph(df, embedding)


class DataFrame:
    def __init__(self, t, d):
        self.title = t
        self.data = d


if __name__ == "__main__":
    print('hello')
    mnist = pd.read_csv(
        'https://www.openml.org/data/get_csv/52667/mnist_784.csv')

    coil_20 = pd.read_csv(
        'https://raw.githubusercontent.com/vaksakalli/datasets/master/coil20.csv')

    fmnist = pd.read_csv('/content/drive/MyDrive/train.csv')
    fmnist = fmnist.drop('Id', axis=1)

    googlenews = load('word2vec-google-news-300').vectors

    pca = PCA(n_components=2, random_state=20)

    dataframes = [DataFrame('MNIST', mnist), DataFrame(
        'Coil-20'), DataFrame('Fashion MNIST', fmnist), DataFrame('Google News', googlenews)]

    for i in range(len(dataframes)):
        UMAPAlgorithm(dataframes[i])
        TSNEAlgorithm(dataframes[i])
        PCAAlgorithm(dataframes[i])
