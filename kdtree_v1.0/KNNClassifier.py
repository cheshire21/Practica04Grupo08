from pandas.core.frame import DataFrame
from node import Node
from kdtree import KDTree
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

class KNNClassifier(object):

    def __init__(self, k):
        self.tree = None
        self.k = k
    
    def fit(self,X_train, Y_train):
        self.tree = KDTree(X_train,Y_train)

    
    def predict(self,X_test):
        pred_y = []
        for i in range(len(X_test)):
            knodes,_ = self.tree.KNN(X_test[i],self.tree.root,self.k,0)
            kneirbors = [node.get_label() for node in knodes]
            # print(X_test[i])
            # print(kneirbors)
            if (self.k % 2 == 0):
                pred_y.append(kneirbors[0])
            else:
                moda=stats.mode(kneirbors)
                # print(moda[0][0])
                pred_y.append(moda[0][0])

        return pred_y

def main():
    #lee el archivo
    # data_prueba = pd.read_csv('./test/Iris.csv')
    data_prueba = pd.read_csv('./test/Iris2_ds.csv')
    # print (data_prueba)
    # Etiquetamos la variable objetivo
    data_prueba.Species = pd.factorize(data_prueba.Species)[0]
    # arr = np.random.permutation(data_prueba.shape[0])


    #arreglo de columnas 
    feature_columns = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm','PetalWidthCm']
    
    X = data_prueba[feature_columns].values
    y = data_prueba['Species'].values

    # X = X[arr]
    # y = y[arr]

    # Separando en train y test

    Xtrain, Xtest, Ytrain, Ytest = train_test_split(X,y,test_size=0.3, random_state=4)

    KnnCla = KNNClassifier(3)
    KnnCla.fit(Xtrain,Ytrain)
