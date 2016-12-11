import numpy as np
from sklearn.datasets import load_iris
from sklearn import tree

"""
Basic ML concept implementation
"""

iris = load_iris()
print(iris.feature_names)
print(iris.target_names)

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

print("   Actual: %s" % test_target)
print("Predicted: %s" % predicted_data)

assert (test_target == predicted_data).all()
