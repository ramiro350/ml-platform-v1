from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

def get_model(algorithm_name, **kwargs):
    if algorithm_name == 'RandomForest':
        return RandomForestClassifier(**kwargs)
    elif algorithm_name == 'SVM':
        return SVC(**kwargs)
    elif algorithm_name == 'LogisticRegression':
        return LogisticRegression(**kwargs)
    else:
        raise ValueError(f"Algoritmo {algorithm_name} não é suportado.")
