

from sklearn.linear_model import LogisticRegression

from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn import datasets
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz

# cargamos los datos
iris = datasets.load_iris()
X = iris.data[:, [2, 3]]
y = iris.target

# Separamos los datos de train
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.3, random_state=0)

# Estandarizamos el train y test (0,1) y desviación tipica
sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

# Pruebas con gamma 0.2,10,50
tree = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=0)
tree.fit(X_train, y_train)



y_pred = tree.predict(X_test_std)




print('Misclassified samples: %d' % (y_test != y_pred).sum())


print('Accuracy: %.2f' % accuracy_score(y_test, y_pred))

def plot_decision_regions(X, y, classifier, test_idx=None, resolution=0.02):
    # setup marker generator and color map

    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])
    # plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                        np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())
    # plot all samples
    for idx, cl in enumerate(np.unique(y)):
       plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1],
                   alpha=0.8, c=cmap(idx),
                   marker=markers[idx], label=cl)
    # highlight test samples
    if test_idx:
       X_test, y_test = X[test_idx, :], y[test_idx]
       plt.scatter(X_test[:, 0], X_test[:, 1], c='',
               alpha=1.0, linewidths=1, marker='o',
               s=55, label='test set')


# Cambiar en cada metodo
X_combined = np.vstack((X_train, X_test))
y_combined = np.hstack((y_train, y_test))
plot_decision_regions(X_combined, y_combined, classifier=tree, test_idx=range(105,150))
plt.xlabel('petal length [cm]')
plt.ylabel('petal width [cm]')
plt.legend(loc='upper left')
#plt.show()


export_graphviz(tree, label=iris.target_names,out_file='tree.dot',feature_names=['petal length', 'petal width'])
