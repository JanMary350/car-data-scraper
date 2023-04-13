import sklearn as sk
import sklearn.model_selection
import sklearn.linear_model
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
data = pd.read_csv('data_volkswagen_golf_100.csv')
data = data.dropna()
print(data.head())
print(data.info())
print(data.describe())
sns.pairplot(data, hue = 'fuel')
plt.show()
sns.heatmap(data.corr(), annot = True)
plt.show()

"""creating model"""
def train_model():
    data = pd.read_csv('data_volkswagen_golf_100.csv')
    data = data.dropna()
    X = np.asarray(data[["year", "kilometers", "engine_size"]])
    Y = np.asarray(data["price"])
    X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.33, shuffle= True)
    regresion = sklearn.linear_model.LinearRegression()
    regresion.fit(X_train, Y_train)
    plt.plot(regresion.predict(X_test), color="green")
    plt.plot(Y_test)
    plt.show()
    print(regresion.predict([[2010, 108800, 1390]]))
