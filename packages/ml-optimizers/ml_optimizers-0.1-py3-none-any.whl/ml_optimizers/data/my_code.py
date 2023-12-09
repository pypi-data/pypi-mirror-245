"""## Stochastic Gradient Descent"""


import numpy as np
from sklearn.metrics import r2_score

# Given functions
def grad_w(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    dw = alpha * (y - yhat) * yhat * (1 - yhat) * x
    return dw

def grad_b(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    db = alpha * (y - yhat) * yhat * (1 - yhat)
    return db

def perceptron(x, w, b):
    yin = x * w + b
    ynet = sigmoid(yin)
    return ynet

def sigmoid(yin):
    ynet = 1 / (1 + np.exp(-yin))
    return ynet

# Stochastic Gradient Descent with metrics
def stochastic_gradient_descent(X, Y, w, b, epochs, alpha):
    wlist, blist, losslist, accuracylist = [w], [b], [], []

    for epoch in range(epochs):
        total_loss, correct_predictions = 0, 0
        yhat_list=[]
        for x, y in zip(X, Y):
            yhat = perceptron(x, w, b)
            loss = y - yhat
            total_loss += loss ** 2
            yhat_list.append(yhat)

            # Update weights and bias
            w += grad_w(w, b, x, y, alpha)
            b += grad_b(w, b, x, y, alpha)

        avg_loss = total_loss / len(X)
        accuracy = r2_score(Y,yhat_list)

        losslist.append(avg_loss)
        accuracylist.append(accuracy)
        wlist.append(w)
        blist.append(b)

    return w, b, wlist, blist, losslist, accuracylist

# Example usage
X = [0.5, 2.5]
Y = [0.2, 0.9]
w, b = 0.0, 0.0  # Initial weights and bias
epochs = 3000
alpha = 0.01  # Learning rate

# Perform stochastic gradient descent
final_w, final_b, wlist, blist, losslist, accuracylist = stochastic_gradient_descent(X, Y, w, b, epochs, alpha)

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

import matplotlib.pyplot as plt
plt.plot(blist[1:],losslist)
plt.title('Bias over loss')

import matplotlib.pyplot as plt
plt.plot(wlist[1:],losslist)
plt.title('Weight over loss')

"""# Mini Batch Gradient Descent"""

import numpy as np
from sklearn.metrics import r2_score

# Given functions
def grad_w(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    dw = alpha * (y - yhat) * yhat * (1 - yhat) * x
    return dw

def grad_b(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    db = alpha * (y - yhat) * yhat * (1 - yhat)
    return db

def perceptron(x, w, b):
    yin = x * w + b
    ynet = sigmoid(yin)
    return ynet

def sigmoid(yin):
    ynet = 1 / (1 + np.exp(-yin))
    return ynet

def mini_batch_gradient_descent(X, Y, w, b, epochs, batchsize, alpha):
    wlist, blist, losslist, accuracylist = [w], [b], [], []

    for i in range(epochs):
      dw,db,sampleno=0,0,0
      total_loss, correct_predictions = 0, 0
      yhat_list=[]
      for x,y in zip(X,Y):
        yhat = perceptron(x, w, b)
        loss = y - yhat
        total_loss += loss ** 2
        yhat_list.append(yhat)

        dw+=grad_w(w,b,x,y,alpha)
        db+=grad_b(w,b,x,y,alpha)
        sampleno+=1
        if sampleno % batchsize == 0:
          w=w+alpha*dw
          b=b+alpha*db
      avg_loss = total_loss / len(X)
      accuracy = r2_score(Y,yhat_list)

      losslist.append(avg_loss)
      accuracylist.append(accuracy)
      wlist.append(w)
      blist.append(b)

    return w, b, wlist, blist, losslist, accuracylist

X = [0.5, 2.5]
Y = [0.2, 0.9]
w, b = 0.0, 0.0  # Initial weights and bias
epochs = 3000
alpha = 0.1  # Learning rate

# Perform Mini Batch gradient descent
final_w, final_b, wlist, blist, losslist, accuracylist = mini_batch_gradient_descent(X, Y, w, b, epochs, 1, alpha)

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

import matplotlib.pyplot as plt
plt.plot(blist[1:],losslist)
plt.title('Bias over loss')

import matplotlib.pyplot as plt
plt.plot(wlist[1:],losslist)
plt.title('Weight over loss')

"""# Batch Gradient Descent"""

import numpy as np
from sklearn.metrics import r2_score

# Given functions
def grad_w(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    dw = alpha * (y - yhat) * yhat * (1 - yhat) * x
    return dw

def grad_b(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    db = alpha * (y - yhat) * yhat * (1 - yhat)
    return db

def perceptron(x, w, b):
    yin = x * w + b
    ynet = sigmoid(yin)
    return ynet

def sigmoid(yin):
    ynet = 1 / (1 + np.exp(-yin))
    return ynet

def batch_gradient_descent(X, Y, w, b, epochs, alpha):
    wlist, blist, losslist, accuracylist = [w], [b], [], []

    for i in range(epochs):
      dw,db,sampleno=0,0,0
      total_loss=0
      yhat_list=[]
      for x,y in zip(X,Y):
        yhat = perceptron(x, w, b)
        loss = y - yhat
        total_loss += loss ** 2
        yhat_list.append(yhat)

        dw+=grad_w(w,b,x,y,alpha)
        db+=grad_b(w,b,x,y,alpha)
        sampleno+=1

      w=w+alpha*dw
      b=b+alpha*db

      avg_loss = total_loss / len(X)
      accuracy = r2_score(Y,yhat_list)

      losslist.append(avg_loss)
      accuracylist.append(accuracy)
      wlist.append(w)
      blist.append(b)

    return w, b, wlist, blist, losslist, accuracylist

X = [0.5, 2.5]
Y = [0.2, 0.9]
w, b = 0.0, 0.0  # Initial weights and bias
epochs = 3000
alpha = 0.1  # Learning rate

# Perform Batch gradient descent
final_w, final_b, wlist, blist, losslist, accuracylist = batch_gradient_descent(X, Y, w, b, epochs, alpha)

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

import matplotlib.pyplot as plt
plt.plot(blist[1:],losslist)
plt.title('Bias over loss')

import matplotlib.pyplot as plt
plt.plot(wlist[1:],losslist)
plt.title('Weight over loss')

"""# Momentum Gradient Descent"""

import numpy as np
from sklearn.metrics import r2_score

# Given functions
def grad_w(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    dw = alpha * (y - yhat) * yhat * (1 - yhat) * x
    return dw

def grad_b(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    db = alpha * (y - yhat) * yhat * (1 - yhat)
    return db

def perceptron(x, w, b):
    yin = x * w + b
    ynet = sigmoid(yin)
    return ynet

def sigmoid(yin):
    ynet = 1 / (1 + np.exp(-yin))
    return ynet

def momentum_gradient_descent(X, Y, w, b, epochs, alpha, beta):
    wlist, blist, losslist, accuracylist = [w], [b], [], []
    vw,vb=0,0
    for i in range(epochs):
      dw,db=0,0
      total_loss=0
      yhat_list=[]
      for x,y in zip(X,Y):
        yhat = perceptron(x, w, b)
        loss = y - yhat
        total_loss += loss ** 2
        yhat_list.append(yhat)

        dw+=grad_w(w,b,x,y,alpha)
        db+=grad_b(w,b,x,y,alpha)

      vw=beta*vw+(1-beta)*dw
      vb=beta*vb+(1-beta)*db
      w=w+alpha*vw
      b=b+alpha*vb

      avg_loss = total_loss / len(X)
      accuracy = r2_score(Y,yhat_list)

      losslist.append(avg_loss)
      accuracylist.append(accuracy)
      wlist.append(w)
      blist.append(b)

    return w, b, wlist, blist, losslist, accuracylist

X = [0.5, 2.5]
Y = [0.2, 0.9]
w, b = 0.0, 0.0  # Initial weights and bias
epochs = 3000
alpha = 0.1  # Learning rate
beta = 0.9

# Perform Momentum gradient descent
final_w, final_b, wlist, blist, losslist, accuracylist = momentum_gradient_descent(X, Y, w, b, epochs, alpha, beta)

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

import matplotlib.pyplot as plt
plt.plot(blist[1:],losslist)
plt.title('Bias over loss')

import matplotlib.pyplot as plt
plt.plot(wlist[1:],losslist)
plt.title('Weight over loss')

"""# Adagrad Gradient Descent"""

import numpy as np
from sklearn.metrics import r2_score

# Given functions
def grad_w(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    dw = alpha * (y - yhat) * yhat * (1 - yhat) * x
    return dw

def grad_b(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    db = alpha * (y - yhat) * yhat * (1 - yhat)
    return db

def perceptron(x, w, b):
    yin = x * w + b
    ynet = sigmoid(yin)
    return ynet

def sigmoid(yin):
    ynet = 1 / (1 + np.exp(-yin))
    return ynet

def adagrad_gradient_descent(X, Y, w, b, epochs, alpha, eps):
    wlist, blist, losslist, accuracylist = [w], [b], [], []
    dw_cache, db_cache = 0, 0

    for i in range(epochs):
        dw, db, total_loss = 0, 0, 0
        yhat_list=[]
        for x, y in zip(X, Y):
            yhat = perceptron(x, w, b)
            loss = y - yhat
            total_loss += loss ** 2
            yhat_list.append(yhat)

            dw += grad_w(w, b, x, y, alpha)
            db += grad_b(w, b, x, y, alpha)

        dw_cache += dw ** 2
        db_cache += db ** 2

        w += alpha / (np.sqrt(dw_cache) + eps) * dw
        b += alpha / (np.sqrt(db_cache) + eps) * db

        avg_loss = total_loss / len(X)
        accuracy = r2_score(Y,yhat_list)

        losslist.append(avg_loss)
        accuracylist.append(accuracy)
        wlist.append(w)
        blist.append(b)

    return w, b, wlist, blist, losslist, accuracylist

X = [0.5, 2.5]
Y = [0.2, 0.9]
w, b = 0.0, 0.0  # Initial weights and bias
epochs = 1000
alpha = 0.1  # Learning rate
eps = 1e-8

# Perform Adagrad gradient descent
final_w, final_b, wlist, blist, losslist, accuracylist = adagrad_gradient_descent(X, Y, w, b, epochs, alpha, eps)

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

import matplotlib.pyplot as plt
plt.plot(blist[1:],losslist)
plt.title('Bias over loss')

import matplotlib.pyplot as plt
plt.plot(wlist[1:],losslist)
plt.title('Weight over loss')

"""# AdaDelta Gradient Descent"""

import numpy as np
from sklearn.metrics import r2_score

# Given functions
def grad_w(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    dw = alpha * (y - yhat) * yhat * (1 - yhat) * x
    return dw

def grad_b(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    db = alpha * (y - yhat) * yhat * (1 - yhat)
    return db

def perceptron(x, w, b):
    yin = x * w + b
    ynet = sigmoid(yin)
    return ynet

def sigmoid(yin):
    ynet = 1 / (1 + np.exp(-yin))
    return ynet

def adadelta_gradient_descent(X, Y, w, b, epochs, rho, eps):
    wlist, blist, losslist, accuracylist = [w], [b], [], []
    dw_cache, db_cache = 0, 0
    dw_adjusted, db_adjusted = 0, 0

    for i in range(epochs):
        dw, db, total_loss = 0, 0, 0
        yhat_list=[]

        for x, y in zip(X, Y):
            yhat = perceptron(x, w, b)
            loss = y - yhat
            total_loss += loss ** 2
            yhat_list.append(yhat)

            dw += grad_w(w, b, x, y, 1)
            db += grad_b(w, b, x, y, 1)

        # Accumulate gradient
        dw_cache = rho * dw_cache + (1 - rho) * dw ** 2
        db_cache = rho * db_cache + (1 - rho) * db ** 2

        # Compute update
        dw_update = - (np.sqrt(dw_adjusted + eps) / np.sqrt(dw_cache + eps)) * dw
        db_update = - (np.sqrt(db_adjusted + eps) / np.sqrt(db_cache + eps)) * db

        # Accumulate updates
        dw_adjusted = rho * dw_adjusted + (1 - rho) * dw_update ** 2
        db_adjusted = rho * db_adjusted + (1 - rho) * db_update ** 2

        # Apply updates
        w -= dw_update
        b -= db_update

        avg_loss = total_loss / len(X)
        accuracy = r2_score(Y,yhat_list)

        losslist.append(avg_loss)
        accuracylist.append(accuracy)
        wlist.append(w)
        blist.append(b)

    return w, b, wlist, blist, losslist, accuracylist

# Example usage
X = [0.5, 2.5]
Y = [0.2, 0.9]
w, b = 0.0, 0.0  # Initial weights and bias
epochs = 3000
rho = 0.95  # Decay rate
eps = 1e-6  # Epsilon for numerical stability

# Perform Adadelta gradient descent
final_w, final_b, wlist, blist, losslist, accuracylist = adadelta_gradient_descent(X, Y, w, b, epochs, rho, eps)

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

import matplotlib.pyplot as plt
plt.plot(blist[1:],losslist)
plt.title('Bias over loss')

import matplotlib.pyplot as plt
plt.plot(wlist[1:],losslist)
plt.title('Weight over loss')

"""# Nesterov Accelerated Gradient Descent"""

import numpy as np
from sklearn.metrics import r2_score

# Given functions
def grad_w(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    dw = alpha * (y - yhat) * yhat * (1 - yhat) * x
    return dw

def grad_b(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    db = alpha * (y - yhat) * yhat * (1 - yhat)
    return db

def perceptron(x, w, b):
    yin = x * w + b
    ynet = sigmoid(yin)
    return ynet

def sigmoid(yin):
    ynet = 1 / (1 + np.exp(-yin))
    return ynet

def NAG_gradient_descent(X, Y, w, b, epochs, alpha, beta):
    wlist, blist, losslist, accuracylist = [w], [b], [], []
    vw,vb=0,0

    for i in range(epochs):
      dw,db,vw,vb=0,0,0,0

      total_loss=0
      yhat_list=[]

      vw=beta*vw
      wt=w+vw
      vb=beta*vb
      bt=b+vb

      for x,y in zip(X,Y):
        yhat = perceptron(x, w, b)
        loss = y - yhat
        total_loss += loss ** 2
        yhat_list.append(yhat)

        dw+=grad_w(wt,bt,x,y,alpha)
        db+=grad_b(wt,bt,x,y,alpha)

      w=wt+(1-beta)*dw
      b=bt+(1-beta)*db

      avg_loss = total_loss / len(X)
      accuracy = r2_score(Y,yhat_list)

      losslist.append(avg_loss)
      accuracylist.append(accuracy)
      wlist.append(w)
      blist.append(b)

    return w, b, wlist, blist, losslist, accuracylist


X = [0.5, 2.5]
Y = [0.2, 0.9]
w, b = 0.0, 0.0  # Initial weights and bias
epochs = 3000
alpha = 0.1  # Learning rate
beta = 0.9

# Perform stochastic gradient descent
final_w, final_b, wlist, blist, losslist, accuracylist = momentum_gradient_descent(X, Y, w, b, epochs, alpha, beta)

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

import matplotlib.pyplot as plt
plt.plot(blist[1:],losslist)
plt.title('Bias over loss')

import matplotlib.pyplot as plt
plt.plot(wlist[1:],losslist)
plt.title('Weight over loss')

"""# Adam Gradient Descent"""

import numpy as np
from sklearn.metrics import r2_score

def perceptron(x, w, b):
    yin = x * w + b
    ynet = sigmoid(yin)
    return ynet

def sigmoid(yin):
    return 1 / (1 + np.exp(-yin))

def grad_w(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    dw = alpha * (y - yhat) * yhat * (1 - yhat) * x
    return dw

def grad_b(w, b, x, y, alpha):
    yhat = perceptron(x, w, b)
    db = alpha * (y - yhat) * yhat * (1 - yhat)
    return db

def adam_gradient_descent(X, Y, w, b, epochs, alpha, beta1, beta2, eps):
    wlist, blist, losslist, accuracylist = [w], [b], [], []
    mw, mb, vw, vb = 0, 0, 0, 0

    for i in range(1, epochs + 1):
        dw, db, total_loss = 0, 0, 0
        yhat_list=[]

        for x, y in zip(X, Y):
            yhat = perceptron(x, w, b)
            loss = y - yhat
            total_loss += loss ** 2
            yhat_list.append(yhat)

            dw += grad_w(w, b, x, y, alpha)
            db += grad_b(w, b, x, y, alpha)

        mw = beta1 * mw + (1 - beta1) * dw
        mb = beta1 * mb + (1 - beta1) * db

        vw = beta2 * vw + (1 - beta2) * (dw ** 2)
        vb = beta2 * vb + (1 - beta2) * (db ** 2)

        mw_hat = mw / (1 - beta1 ** i)
        mb_hat = mb / (1 - beta1 ** i)
        vw_hat = vw / (1 - beta2 ** i)
        vb_hat = vb / (1 - beta2 ** i)

        w += alpha / (np.sqrt(vw_hat) + eps) * mw_hat
        b += alpha / (np.sqrt(vb_hat) + eps) * mb_hat

        avg_loss = total_loss / len(X)
        accuracy = r2_score(Y,yhat_list)

        losslist.append(avg_loss)
        accuracylist.append(accuracy)
        wlist.append(w)
        blist.append(b)

    return w, b, wlist, blist, losslist, accuracylist

# Example usage
X = [0.5, 2.5]
Y = [0.2, 0.9]
w, b = 0.0, 0.0  # Initial weights and bias
epochs = 3000
alpha = 0.01  # Learning rate
beta1 = 0.9  # Exponential decay rate for the first moment estimates
beta2 = 0.999  # Exponential decay rate for the second moment estimates
eps = 1e-8  # Epsilon for numerical stability

# Perform Adam gradient descent
final_w, final_b, wlist, blist, losslist, accuracylist = adam_gradient_descent(X, Y, w, b, epochs, alpha, beta1, beta2, eps)

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

import matplotlib.pyplot as plt
plt.plot(blist[1:],losslist)
plt.title('Bias over loss')

import matplotlib.pyplot as plt
plt.plot(wlist[1:],losslist)
plt.title('Weight over loss')