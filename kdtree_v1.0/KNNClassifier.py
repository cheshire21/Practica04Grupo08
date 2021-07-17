from node import Node
from kdtree import KDTree


class KNNClassifier:

    def __init__(self):
        self.tree = None

    def fit(self,X_train, Y_train):
        self.tree = KDTree(X_train,Y_train)

    def predict(self,X_test):
        for i in range(len(X_test)):
            knodes,_ = self.tree.KNN(X_test[i])

    