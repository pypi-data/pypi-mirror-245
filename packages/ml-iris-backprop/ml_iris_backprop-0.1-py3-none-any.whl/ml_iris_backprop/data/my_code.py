import numpy as np

from sklearn import datasets

from sklearn.model_selection import train_test_split

def perceptron(x, w, b):
    yin = np.dot(x, w) + b
    ynet = sigmoid(yin)
    return ynet

def sigmoid(yin):
    return 1 / (1 + np.exp(-yin))

def dw(x, y, w, b, alpha):
    yhat = perceptron(x, w, b)
    loss = y - yhat
    dw = alpha * (y - yhat) * yhat * (1 - yhat) * x
    return loss, dw

def db(x, y, w, b, alpha):
    yhat = perceptron(x, w, b)
    db = alpha * (y - yhat) * yhat * (1 - yhat)
    return db

def accuracy(y_true, y_pred):
    correct_predictions = np.sum(y_true == y_pred)
    total_predictions = len(y_true)
    return correct_predictions / total_predictions

def stoch_with_accuracy(X, Y, w, b, epochs, alpha):
    wlist = [w.copy()]
    blist = [b]
    losslist = []
    accuracylist = []

    for i in range(epochs):
        total_loss = 0
        predictions = []
        for x, y in zip(X, Y):
            loss, wup = dw(x, y, w, b, alpha)
            w += wup
            b += db(x, y, w, b, alpha)
            total_loss += loss ** 2
            predictions.append(np.round(perceptron(x, w, b)))  # Predicted class

        avg_loss = total_loss / len(X)
        acc = accuracy(Y, np.array(predictions))
        losslist.append(avg_loss)
        accuracylist.append(acc)
        wlist.append(w.copy())
        blist.append(b)

    return w, b, wlist, blist, losslist, accuracylist

iris = datasets.load_iris()

X=iris.data
y=iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
w=[0 for i in range(len(X[0]))]
b=0
w,b,wlist,blist,losslist,accuracylist=stoch_with_accuracy(X_train,y_train,w,b,100,0.001)

import matplotlib.pyplot as plt
plt.plot(wlist)
plt.title('Change in Weight')

import matplotlib.pyplot as plt
plt.plot(blist)
plt.title('Change in Bias')

import matplotlib.pyplot as plt
plt.plot(losslist)
plt.title('MSE')

import matplotlib.pyplot as plt
plt.plot(accuracylist)
plt.title('Accuracy')

predictions=[]
for x in X_test:
  predictions.append(np.round(perceptron(x, w, b)))

from sklearn.metrics import classification_report
print(classification_report(predictions,y_test))