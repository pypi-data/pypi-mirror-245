"""
## Principle Component Analysis

Importing required libraries
"""

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.preprocessing import MinMaxScaler

"""Loading the Dataset"""

iris = datasets.load_iris()

X = iris.data
y = iris.target
print("X:",X[0])
target_names = iris.target_names

"""Scaling data using MinMaxScaler"""

scaler = MinMaxScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)

"""Defining a function to plot PCA for different targets"""

def plot3clusters(X, title, vtitle):
    plt.figure()
    colors = ['navy','turquoise','darkorange']
    for color, i, target_name in zip(colors, [0,1,2], target_names):
        plt.scatter(X[y==i, 0], X[y==i, 1], color=color, label=target_name)
        plt.legend(loc='upper left')
        plt.title(title)
        plt.xlabel(vtitle + "1")
        plt.ylabel(vtitle + "2")
        plt.show()

"""Implementing and visualizing PCA"""

pca = PCA()
pca_transformed = pca.fit_transform(X_scaled)

# Displaying new Transformed Values
print("Pca transformed: ", pca_transformed[0])

# Calling the plotting function
plot3clusters(pca_transformed[:,:2], 'PCA', 'PC')