import numpy as np
from sklearn.datasets import load_iris
from sklearn import tree

"""
Basic ML concept implementation

Test explains how sklearn machine learning works using iris example
"""
def test_sklearn_decision_tree_classifier():
    iris = load_iris()
    # iris.feature_names - available characteristics of iris
    # iris.target_names - available types of iris

    test_idx = [0, 50, 100]
    # Remove elements to create 'food' for machine learning
    training_target = np.delete(iris.target, test_idx)
    train_data = np.delete(iris.data, test_idx, axis=0)

    # Use removed elements to create test data
    test_target = iris.target[test_idx]
    test_data = iris.data[test_idx]

    clf = tree.DecisionTreeClassifier()
    clf.fit(train_data, training_target)

    predicted_data = clf.predict(test_data)

    assert (test_target == predicted_data).all()
