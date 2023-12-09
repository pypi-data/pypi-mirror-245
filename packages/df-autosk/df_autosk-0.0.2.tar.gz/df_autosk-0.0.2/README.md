# DF for AutoSklearn

Extension of AutoSklearnClassifier with DF21 - [CascadeForestClassifier](https://deep-forest.readthedocs.io/en/latest/index.html) - a Deep Forest implementantion. Based on an [example extension](https://automl.github.io/auto-sklearn/master/examples/80_extending/example_extending_classification.html#sphx-glr-download-examples-80-extending-example-extending-classification-py) from Auto-Sklearn documentation.

## Requirements

* Linux operating system (requirement of Auto-Sklearn)
* numpy version <= 1.19
* installation of CascadeForestClassifier
* installation of [Auto-Sklearn](https://automl.github.io/auto-sklearn/master/installation.html)
* input variables have to be converted to numeric without missing values 
* output variables also should be converted to numeric values (you can use sklearn LabelEncoder)

## Example use

```
# import libraries
import sklearn.metrics
import autosklearn.classification
import autosklearn.pipeline.components.classification


# import DFClassifier
from df_autosk.df_autosk import DFClassifier

# add DFClassifier to autosklearn classifier
autosklearn.pipeline.components.classification.add_classifier(DFClassifier)

# initialize and get hyperparameter search space
cs = DFClassifier.get_hyperparameter_search_space()
print(cs)

# load the dataset
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# use the classifier
clf = autosklearn.classification.AutoSklearnClassifier(
        	time_left_for_this_task=5400,
        	include={"classifier": ['DFClassifier']},
        	initial_configurations_via_metalearning=0,
        	memory_limit = 102400,
                # Not recommended for a real implementation
               	smac_scenario_args={"runcount_limit": 2}
                )

clf.fit(X_train, y_train)

#get result
y_pred = clf.predict(X_test)
print("accuracy: ", sklearn.metrics.accuracy_score(y_pred, y_test))
```
Example based on an [example extension](https://automl.github.io/auto-sklearn/master/examples/80_extending/example_extending_classification.html#sphx-glr-download-examples-80-extending-example-extending-classification-py) from Auto-Sklearn documentation.