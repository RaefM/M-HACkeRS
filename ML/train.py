
import pandas as pd
import numpy as np
import json
import pickle
import datetime

from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn import metrics
from matplotlib import pyplot as plt


"""
DEPENDENCY SETUP INSTRUCTIONS
pip install pandas
pip install numpy
pip install matplotlib
pip install -U scikit-learn
"""

def openJSON(fname):
  f = open(fname)
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
    return LinearSVC(penalty = 'l1', dual = False, C = c,class_weight = 'balanced')
  else:
    return SVC(kernel = 'linear', C = c, class_weight = 'balanced', degree = degree)


"""
Returns a polynomial SVM classifier with the specified hyperparameter values
"""
def create_poly_classifier(degree=2, c=1.0, r=0.0, decision_function_shape='ovr'):
  return SVC(kernel='poly', degree = 2, C = c, coef0 = r, class_weight = 'balanced', gamma = 'auto')


"""
May not be relevant. As per scikit learn, use the GridSearchCV method
"""
def create_rbf_classifier(c=1.0, gamma=0.0, decision_function_shape='ovr'):
  return SVC(kernel='rbf', C = c, class_weight = 'balanced', gamma = gamma)

def performance(y_true, Y_pred, metric="accuracy"):
    """Calculate performance metrics.

    Performance metrics are evaluated on the true labels y_true versus the
    predicted labels Y_pred.

    Input:
        y_true: (n,) array containing known labels
        Y_pred: (n,) array containing predicted scores
        metric: string specifying the performance metric (default='accuracy'
                 other options: 'f1-score', 'auroc', 'precision', 'sensitivity',
                 and 'specificity')
    Returns:
        the performance as an np.float64
    """
    # TODO: Implement this function
    # This is an optional but very useful function to implement.
    # See the sklearn.metrics documentation for pointers on how to implement
    # the requested metrics.
    if metric == "accuracy":
        return metrics.accuracy_score(y_true,Y_pred)
    elif metric == "f1-score":
        return metrics.f1_score(y_true, Y_pred)
    elif metric == "auroc":
        return metrics.roc_auc_score(y_true, Y_pred)
    elif metric == "precision":
        return metrics.precision_score(y_true,Y_pred)
    elif metric == "sensitivity":
        tn, fp, fn, tp = metrics.confusion_matrix(y_true, Y_pred , labels= [-1,1]).ravel()
        return tp/(tp + fn)
    elif metric == "specificity":
        tn, fp, fn, tp = metrics.confusion_matrix(y_true, Y_pred, labels= [-1,1]).ravel()
        return tn/(tn + fp)

      
"""
Compute performance with the specified metric
"""
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

"""
Returns: average performance on the stipulated metric across all k folds
"""
def cv_performance(clf, X, y, k=4, metric="accuracy"):
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

def cv_performance_multiclass(clf, X, y, k=4, metric="accuracy"):
    """Split data into k folds and run cross-validation.

    Splits the data X and the labels y into k-folds and runs k-fold
    cross-validation: for each fold i in 1...k, trains a classifier on
    all the data except the ith fold, and tests on the ith fold.
    Calculates and returns the k-fold cross-validation performance metric for
    classifier clf by averaging the performance across folds.
    Input:
        clf: an instance of SVC()
        X: (n,d) array of feature vectors, where n is the number of examples
           and d is the number of features
        y: (n,) array of binary labels {1,-1}
        k: an int specifying the number of folds (default=5)
        metric: string specifying the performance metric (default='accuracy'cross validation
             other options: 'f1-score', 'auroc', 'precision', 'sensitivity',
             and 'specificity')
    Returns:
        average 'test' performance across the k folds as np.float64
    """
    # TODO: Implement this function
    # HINT: You may find the StratifiedKFold from sklearn.model_selection
    # to be useful

    # Put the performance of the model on each fold in the scores array
    scores = []
    skf = StratifiedKFold(n_splits=k, random_state=None, shuffle=False)
    for train_index, test_index in skf.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        clf.fit(X_train, y_train)
        if metric == "auroc":
            prediction = clf.decision_function(X_test)
            iter_performance = performance(y_test, prediction, metric)
            scores.append(iter_performance)
        else:
            prediction = clf.predict(X_test)
            iter_performance = performance(y_test, prediction, metric)
            scores.append(iter_performance)
    return np.array(scores).mean()


def update_logs(loglines, newLog):
  print(newLog)
  loglines.append(newLog)
  return


def select_param_general(get_svc, X, y, k=4, metric="accuracy", param_range=[], param_names='C'):
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
def select_param_linear(X, y, k=4, penalty='l2', metric="accuracy", param_range=[]):
  def get_svc(curr_params):
    return create_linear_classifier(penalty=penalty, c=curr_params)
  
  return select_param_general(get_svc, X, y, k, metric, param_range)


def select_param_linear_multiclass(
    X, y, k=4, metric="accuracy", param_range=[], loss="hinge", penalty="l2", dual=True
):
    """Search for hyperparameters of linear SVM with best k-fold CV performance.

    Sweeps different settings for the hyperparameter of a linear-kernel SVM,
    calculating the k-fold CV performance for each setting on X, y.
    Input:
        X: (n,d) array of feature vectors, where n is the number of examples
        and d is the number of features
        y: (n,) array of binary labels {1,-1}
        k: int specifying the number of folds (default=5)
        metric: string specifying the performance metric (default='accuracy',
             other options: 'f1-score', 'auroc', 'precision', 'sensitivity',
             and 'specificity')
        C_range: an array with C values to be searched over
        loss: string specifying the loss function used (default="hinge",
             other option of "squared_hinge")
        penalty: string specifying the penalty type used (default="l2",
             other option of "l1")
        dual: boolean specifying whether to use the dual formulation of the
             linear SVM (set True for penalty "l2" and False for penalty "l1"ß)
    Returns:
        the parameter value for a linear-kernel SVM that maximizes the
        average 5-fold CV performance.
    """
    # TODO: Implement this function
    # HINT: You should be using your cv_performance function here
    # to evaluate the performance of each SVM
    print("running")
    max_performance = 0
    max_c = 0
    log = []
    for i in param_range:
        clf = OneVsRestClassifier(LinearSVC(penalty,loss,dual,C=i,random_state=445))
        perf = cv_performance_multiclass(clf,X,y,k,metric)
        update_logs(log, 'For C = ' + str(param_val) + ' ' + metric + ' had performance = ' + str(perf) + '\n')
        if perf > max_performance:
            max_performance = perf
            max_c = i
    print(max_c)
    print(max_performance)
    return max_c

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
def select_param_rbf(X, y, k=4, metric="accuracy", param_range=[]):
  def get_svc(curr_params):
    C, gamma = curr_params
    return create_rbf_classifier(c=C, gamma=gamma)
  
  return select_param_general(get_svc, X, y, k, metric, param_range, "(C, gamma)")


"""
Sweeps the provided range of hyperparameter values and returns the hyperparameter value providing the best performance
Uses a quadratic kernel SVM

param range should include (C,r) pairs
"""
def select_param_poly(X, y, degree=2, k=4, metric="accuracy", param_range=[]):
  def get_svc(curr_params):
    C, r = curr_params
    return create_poly_classifier(degree=degree, c=C, r=r)
  
  return select_param_general(get_svc, X, y, k, metric, param_range, "(C, r)")

# Returns a grid of dimensions (pows*2, ) consisting of powers of 10 from 10^-(pows) to 10^(pows)
def get_exp_grid(pows=6):
  exp_range = []

  for pow in range(pows):
    exp_range.append(10**(-pow))

  for pow in range(pows):
    exp_range.append(10**(pow))

  return exp_range

# Returns a grid of dimensions (pows*2, pows*2) consisting of all pairs of powers of 10 from 10^-(pows) to 10^(pows)
def get_exp_grid_square(pows=6):
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
  print("linear 1 start")
  now = datetime.datetime.now()
  print(now)
  with open("linearHyperParamL1.txt", "w") as file:
    best_param_vals, log = select_param_linear(X=xData, y=yTrue, param_range=hyperparam_grid, penalty='l1')
    update_logs(log, "\n\tBEST VALUES FOR L1 LINEAR (C): " + str(best_param_vals) + "\n")
    file.writelines(log)
  clf = create_linear_classifier(penalty='l1', c=best_param_vals, degree=1, decision_function_shape='ovr')
  clf.fit(xData,yTrue)
  with open('modellinearHyperParamL1.pkl','wb') as f:
    pickle.dump(clf,f)
  print("linear 1 done")
  
  print("linear 2 start")
  now = datetime.datetime.now()
  print(now)
  with open("linearHyperParamL2.txt", "w") as file:
    best_param_vals, log = select_param_linear(X=xData, y=yTrue, param_range=hyperparam_grid, penalty='l2')
    update_logs(log, "\n\tBEST VALUES FOR L1 LINEAR (C): " + str(best_param_vals) + "\n")
    file.writelines(log)
  clf = create_linear_classifier(penalty='l2', c=best_param_vals, degree=1, decision_function_shape='ovr')
  clf.fit(xData,yTrue)
  with open('modellinearHyperParamL2.pkl','wb') as f:
    pickle.dump(clf,f)
  print("linear 2 done")

  print("quadratic start")
  now = datetime.datetime.now()
  print(now)
  with open("quadraticHyperParamL2.txt", "w") as file:
    best_param_vals, log = select_param_poly(X=xData, y=yTrue, param_range=hyperparam_grid_square, degree=2)
    update_logs(log, "\n\tBEST VALUES FOR QUADRATIC (C, r): " + str(best_param_vals) + "\n")
    file.writelines(log)
  clf = create_poly_classifier(degree=2, c=best_param_vals, r=best_param_vals, decision_function_shape='ovr')
  clf.fit(xData,yTrue)
  with open('modelquadraticL2.pkl','wb') as f:
    pickle.dump(clf,f)
  print("quadratic done")

  print("cubic start")
  now = datetime.datetime.now()
  print(now)
  with open("CubicHyperParamL2.txt", "w") as file:
    best_param_vals, log = select_param_poly(X=xData, y=yTrue, param_range=hyperparam_grid_square, degree=3)
    update_logs(log, "\n\tBEST VALUES FOR CUBIC (C, r): " + str(best_param_vals) + "\n")
    file.writelines(log)
  clf = create_poly_classifier(degree=3, c=best_param_vals, r=best_param_vals, decision_function_shape='ovr')
  clf.fit(xData,yTrue)
  with open('modelCubicL2.pkl','wb') as f:
    pickle.dump(clf,f)
  print("cubic done")

  print("rbf start")
  now = datetime.datetime.now()
  print(now)
  with open("RBFHyperParamL2.txt", "w") as file:
    best_param_vals, log = select_param_rbf(X=xData, y=yTrue, param_range=hyperparam_grid_square)
    update_logs(log, "\n\tBEST VALUES FOR RBF (C, gamma): " + str(best_param_vals) + "\n")
    file.writelines(log)
  clf = create_rbf_classifier(c=best_param_vals, decision_function_shape='ovr', gamma=best_param_vals)
  clf.fit(xData,yTrue)
  with open('modelRbfL2.pkl','wb') as f:
    pickle.dump(clf,f)
  print("rbf done")

  print("linear multiclass start")
  now = datetime.datetime.now()
  print(now)
  with open("linearHyperParamL1.txt", "w") as file:
    best_param_vals, log = select_param_linear_multiclass(X=xData, y=yTrue, param_range=hyperparam_grid, penalty='l2')
    update_logs(log, "\n\tBEST VALUES FOR LINEAR Multiclass (C): " + str(best_param_vals) + "\n")
    file.writelines(log)
  clf = OneVsRestClassifier(LinearSVC(penalty,loss,dual,C=best_param_vals,random_state=445))
  clf.fit(xData,yTrue)
  with open('modellinearMulticlass.pkl','wb') as f:
    pickle.dump(clf,f)
  print("linear multiclass done")