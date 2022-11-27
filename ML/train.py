
import pandas as pd
import numpy as np
import json

from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from matplotlib import pyplot as plt


"""
DEPENDENCY SETUP INSTRUCTIONS
pip install numpy
pip install matplotlib
pip install -U scikit-learn
"""

def openJSON():
  f = open("pitchVectors.json")
  return json.load(f)


"""
Returns two numpy arrays; one containing the training data and the other containing labels
let n = number of songs
Training Data Dims: (n, 12)
Labels: (n,)
"""
def extract_training_data():
  labeledJson = openJSON("normalizedPitchVectors.json")

  xTrain = []
  yTrue = []

  for songName in labeledJson:
    for pitchVector in labeledJson[songName]:
      xTrain.append(pitchVector)
      yTrue.append(songName)

  return np.array(xTrain), np.array(yTrue)


"""
Returns a linear SVM clasifier with the specified hyperparameter values
"""
def create_linear_classifier(penalty='l2', c=1.0, degree=1, decision_function_shape='ovr'):
  if (penalty == 'l1'):
    return LinearSVC(penalty = 'l1', dual = False, C = c,class_weight = 'balanced', decision_function_shape=decision_function_shape)
  else:
    return SVC(kernel = 'linear', C = c, class_weight = 'balanced', degree = degree, decision_function_shape=decision_function_shape)


"""
Returns a polynomial SVM classifier with the specified hyperparameter values
"""
def create_poly_classifier(degree=2, c=1.0, r=0.0, decision_function_shape='ovr'):
  return SVC(kernel='poly', degree = 2, C = c, coef0 = r, class_weight = 'balanced', gamma = 'auto', decision_function_shape=decision_function_shape)


"""
May not be relevant. As per scikit learn, use the GridSearchCV method
"""
def create_rbf_classifier(c=1.0, gamma=0.0, decision_function_shape='ovr'):
  return SVC(kernel='rbf', C = c, class_weight = 'balanced', gamma = gamma, decision_function_shape=decision_function_shape)

"""
Compute performance with the specified metric
"""
def performance(y_true, y_pred, metric="accuracy"):
  conf_mat = confusion_matrix(y_true, y_pred, labels = [1, -1])
  arr_conf_mat = np.array(conf_mat)
  
  if (metric == "accuracy"):
    # add along diagonal and divide by total number of predictions
    # diagonal signifies values that had the same true and predicted value
    np.sum(arr_conf_mat.diagonal()) / np.sum(arr_conf_mat)
  else:
    print("Unsupported performance metric")
    raise(NotImplementedError)

"""
Returns: average performance on the stipulated metric across all k folds
"""
def cv_performance(clf, X, y, k=5, metric="accuracy"):
  stratifiedKFold = StratifiedKFold(n_splits = k)
  scores = []

  # Train and test on each of the stratifications
  for train_i, test_i in stratifiedKFold.split(X,y):
    # fit to training data and make the classifier predict the test data
    clf.fit(X[train_i], y[train_i])
    y_predict_i = clf.predict(X[test_i])

    #store calculated measure
    scores.append(performance(y[test_i], y_predict_i, metric))

  # And return the average performance across all fold splits.
  return np.array(scores).mean()


def update_logs(loglines, newLog):
  print(newLog)
  loglines.append(newLog)
  return


def select_param_general(get_svc, X, y, k=5, metric="accuracy", param_range=[], param_names='C'):
  best_param_vals = 0.0
  best_perf = -1
  log = []

  for param_val in param_range:
    clf_i = get_svc(param_val)
    perf_i = cv_performance(clf_i, X, y, k, metric)

    update_logs(log, 'For ' + param_names +  ' = ' + str(param_val) + ' ' + metric + ' had performance = ' + str(perf_i) + '\n')

    if (perf_i > best_perf):
      best_param_vals = param_val
      best_perf = perf_i

  return best_param_vals, log

"""
Sweeps the provided range of hyperparameter values and returns the hyperparameter value providing the best performance
Uses a linear kernel SVM
"""
def select_param_linear(X, y, k=5, penalty='l2', metric="accuracy", param_range=[]):
  def get_svc(curr_params):
    return create_linear_classifier(penalty=penalty, c=curr_params)
  
  return select_param_general(get_svc, X, y, k, metric, param_range)


"""
Sweeps the provided range of hyperparameter values and returns the hyperparameter value providing the best performance
Uses a gaussian kernel SVM

param_range should include (C,gamma) pairs

From the Scikit-Learn Docs:
When training an SVM with the Radial Basis Function (RBF) kernel, two parameters must be considered: C and gamma. 
The parameter C, common to all SVM kernels, trades off misclassification of training examples against simplicity of the decision surface. 
A low C makes the decision surface smooth, while a high C aims at classifying all training examples correctly. 
gamma defines how much influence a single training example has. The larger gamma is, the closer other examples must be to be affected.
Proper choice of C and gamma is critical to the SVMs performance. 
One is advised to use GridSearchCV with C and gamma spaced exponentially far apart to choose good values.
"""
def select_param_rbf(X, y, k=5, metric="accuracy", param_range=[]):
  def get_svc(curr_params):
    C, gamma = curr_params
    return create_rbf_classifier(c=C, gamma=gamma)
  
  return select_param_general(get_svc, X, y, k, metric, param_range, "(C, gamma)")


"""
Sweeps the provided range of hyperparameter values and returns the hyperparameter value providing the best performance
Uses a quadratic kernel SVM

param range should include (C,r) pairs
"""
def select_param_poly(X, y, degree=2, k=5, metric="accuracy", param_range=[]):
  def get_svc(curr_params):
    C, r = curr_params
    return create_poly_classifier(degree=degree, c=C, r=r)
  
  return select_param_general(get_svc, X, y, k, metric, param_range, "(C, r)")

# Returns a grid of dimensions (pows*2, ) consisting of powers of 10 from 10^-(pows) to 10^(pows)
def get_exp_grid(pows=5):
  exp_range = []

  for pow in range(pows):
    exp_range.append(10**(-pow))

  for pow in range(pows):
    exp_range.append(10**(pow))

  return exp_range

# Returns a grid of dimensions (pows*2, pows*2) consisting of all pairs of powers of 10 from 10^-(pows) to 10^(pows)
def get_exp_grid_square(pows=5):
  exp_range_line = get_exp_grid(pows)
  exp_range_square = []

  for a in exp_range_line:
    for b in exp_range_line:
      exp_range_square.append((a, b))

  return exp_range_square

if __name__ == "__main__":
  xData, yTrue = extract_training_data()
  hyperparam_grid = get_exp_grid()
  hyperparam_grid_square = get_exp_grid_square()

  # Only tests One-vs-Rest classification (this means for each hyperparam val, it'll train num_songs classifiers)
  # We won't use One-vs-One as that'd make it (num_songs)^2 classifiers to train PER HYPERPARAM VALUE which is yikes
  
  with open("linearHyperParamL1.txt", "w") as file:
    best_param_vals, log = select_param_linear(X=xData, y=yTrue, param_range=hyperparam_grid, penalty='l1')
    update_logs(log, "\n\tBEST VALUES FOR L2 LINEAR (C): " + str(best_param_vals) + "\n")
    file.writelines(log)
  
  with open("linearHyperParamL2.txt", "w") as file:
    best_param_vals, log = select_param_linear(X=xData, y=yTrue, param_range=hyperparam_grid, penalty='l2')
    update_logs(log, "\n\tBEST VALUES FOR L1 LINEAR (C): " + str(best_param_vals) + "\n")
    file.writelines(log)

  with open("quadraticHyperParamL2.txt", "w") as file:
    best_param_vals, log = select_param_poly(X=xData, y=yTrue, param_range=hyperparam_grid_square, degree=2)
    update_logs(log, "\n\tBEST VALUES FOR QUADRATIC (C, r): " + str(best_param_vals) + "\n")
    file.writelines(log)

  with open("CubicHyperParamL2.txt", "w") as file:
    best_param_vals, log = select_param_poly(X=xData, y=yTrue, param_range=hyperparam_grid_square, degree=3)
    update_logs(log, "\n\tBEST VALUES FOR CUBIC (C, r): " + str(best_param_vals) + "\n")
    file.writelines(log)

  with open("RBFHyperParamL2.txt", "w") as file:
    best_param_vals, log = select_param_rbf(X=xData, y=yTrue, param_range=hyperparam_grid_square)
    update_logs(log, "\n\tBEST VALUES FOR RBF (C, gamma): " + str(best_param_vals) + "\n")
    file.writelines(log)