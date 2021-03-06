from pandas.core.frame import DataFrame
from node import Node
from kdtree import KDTree
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
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
                moda=stats.mode(kneirbors)
                if(len(moda[0]) > 1):
                    pred_y.append(kneirbors[0])
                else:
                    pred_y.append(moda[0][0])    
            else:
                moda=stats.mode(kneirbors)
                # print(moda[0][0])
                pred_y.append(moda[0][0])

        return pred_y

# def main():
#     #lee el archivo
#     # data_prueba = pd.read_csv('./test/Iris.csv')
#     data_prueba = pd.read_csv('./test/Iris2_ds.csv')
#     # print (data_prueba)
#     # Etiquetamos la variable objetivo
#     data_prueba.Species = pd.factorize(data_prueba.Species)[0]
#     # arr = np.random.permutation(data_prueba.shape[0])


#     #arreglo de columnas 
#     feature_columns = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm','PetalWidthCm']
    
#     X = data_prueba[feature_columns].values
#     y = data_prueba['Species'].values

#     # X = X[arr]
#     # y = y[arr]

#     # Separando en train y test

#     Xtrain, Xtest, Ytrain, Ytest = train_test_split(X,y,test_size=0.3, random_state=4)
    
#     #normalizando data Xtrain
#     Xtrain_md = np.mean(Xtrain,0)
#     std = np.std(Xtrain,0)

#     Xtrain = (Xtrain-Xtrain_md)/std

#     Xtrain_std = np.where(std==0.0,1.0,std)

#     KnnCla = KNNClassifier(3)
#     KnnCla.fit(Xtrain,Ytrain)


#     #estandarizacion data Xtest
#     Xtest = (Xtest - Xtrain_md)/Xtrain_std

#     pred_y = KnnCla.predict(Xtest)
#     pred_y = np.array(pred_y)
#     # print(pred_y)
#     # print(Ytest)

#     cnf_matrix = metrics.confusion_matrix(Ytest,pred_y)
#     print(cnf_matrix)
#     dataframe = pd.DataFrame(cnf_matrix)

#     sns.heatmap(dataframe, annot=True, cbar=None, cmap="Blues")
#     plt.title("Confusion Matrix"), plt.tight_layout()
#     plt.ylabel("True Class"), plt.xlabel("Predicted Class")
#     plt.show()

# main()

def main():
    #lee el archivo
    # data_prueba = pd.read_csv('./test/Iris.csv')
    data_prueba = pd.read_csv('./test/diabetes.csv')

    #arreglo de columnas 
    feature_columns = ['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']
    
    arr = np.random.permutation(data_prueba.shape[0])


    X = data_prueba[feature_columns].values
    y = data_prueba['Outcome'].values

    # Separando en train y test
    Xtrain, Xtest, Ytrain, Ytest = train_test_split(X,y,test_size=0.3, random_state=4)

    #normalizando data Xtrain
    Xtrain_md = np.mean(Xtrain,0)
    std = np.std(Xtrain,0)

    Xtrain = (Xtrain-Xtrain_md)/std

    Xtrain_std = np.where(std==0.0,1.0,std)

    KnnCla = KNNClassifier(3)
    KnnCla.fit(Xtrain,Ytrain)

    #normalizando data Xtest
    Xtest = (Xtest - Xtrain_md)/Xtrain_std

    pred_y = KnnCla.predict(Xtest)
    pred_y = np.array(pred_y)

    print('Accuracy: ', metrics.accuracy_score(Ytest,pred_y))
    print('Precision: ', metrics.precision_score(Ytest,pred_y))

    cnf_matrix = metrics.confusion_matrix(Ytest,pred_y)
    print(cnf_matrix)
    dataframe = pd.DataFrame(cnf_matrix)

    sns.heatmap(dataframe, annot=True, cbar=None, cmap="Blues")
    plt.title("Confusion Matrix"), plt.tight_layout()
    plt.ylabel("True Class"), plt.xlabel("Predicted Class")
    plt.show()


main()
