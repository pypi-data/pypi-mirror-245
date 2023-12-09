# Based on an example extension from Auto-Sklearn documentation
# https://automl.github.io/auto-sklearn/master/examples/80_extending/example_extending_classification.html#sphx-glr-download-examples-80-extending-example-extending-classification-py

from typing import Optional

from ConfigSpace.configuration_space import ConfigurationSpace
from ConfigSpace.hyperparameters import (
    CategoricalHyperparameter,
    UniformIntegerHyperparameter,
    UniformFloatHyperparameter,
)

from deepforest import CascadeForestClassifier

from autosklearn.askl_typing import FEAT_TYPE_TYPE
import autosklearn.classification
import autosklearn.pipeline.components.classification
from autosklearn.pipeline.components.base import AutoSklearnClassificationAlgorithm
from autosklearn.pipeline.constants import (
    DENSE,
    SIGNED_DATA,
    UNSIGNED_DATA,
    PREDICTIONS,
)


class DFClassifier(AutoSklearnClassificationAlgorithm):
    """
    Custom classifier based on CascadeForestClassifier implementing AutoSklearn's base classification algorithm.
    """

    def __init__(
        self,
        n_trees,
        n_estimators,
        criterion,
        bin_type,
        use_predictor,
        predictor,
        random_state=None,
    ):
        """
        Initialize DFClassifier.

        Args:
        - n_trees (int): Number of trees in the cascade forest.
        - n_estimators (int): Number of base estimators in the cascade forest.
        - criterion (str): Criterion for information gain calculation.
        - bin_type (str): Type of binning method.
        - use_predictor (bool): Use predictor or not.
        - predictor (str): Type of predictor.
        - random_state (int, optional): Random seed. Defaults to None.
        """
        self.n_trees = n_trees
        self.n_estimators = n_estimators
        self.criterion = criterion
        self.bin_type = bin_type
        self.use_predictor = use_predictor
        self.predictor = predictor
        self.random_state = random_state

    def fit(self, X, y):
        """
        Fit the model to the given training data.

        Args:
        - X (array-like): Training input samples.
        - y (array-like): Target values.

        Returns:
        - self: Returns an instance of self.
        """
        self.n_trees = int(self.n_trees)
        self.n_estimators = int(self.n_estimators)
        self.bin_type = str(self.bin_type)
        self.criterion = str(self.criterion)
        self.use_predictor = bool(self.use_predictor)
        self.predictor = str(self.predictor)

        self.estimator = CascadeForestClassifier(
            n_trees=self.n_trees,
            n_estimators=self.n_estimators,
            criterion=self.criterion,
            bin_type=self.bin_type,
            use_predictor=self.use_predictor,
            predictor=self.predictor,
            random_state=self.random_state,
        )
        self.estimator.fit(X, y)
        return self

    def predict(self, X):
        """
        Predict the target based on input samples.

        Args:
        - X (array-like): Input samples.

        Returns:
        - array: Predicted targets.
        """
        if self.estimator is None:
            raise NotImplementedError()
        return self.estimator.predict(X)

    def predict_proba(self, X):
        """
        Predict class probabilities for input samples.

        Args:
        - X (array-like): Input samples.

        Returns:
        - array: Predicted probabilities.
        """
        if self.estimator is None:
            raise NotImplementedError()
        return self.estimator.predict_proba(X)

    @staticmethod
    def get_properties(dataset_properties=None):
        """
        Return the properties of the classifier.

        Returns:
        - dict: Classifier properties.
        """
        return {
            "shortname": "DF Classifier",
            "name": "Deep Forest Classifier",
            "handles_regression": False,
            "handles_classification": True,
            "handles_multiclass": True,
            "handles_multilabel": False,
            "handles_multioutput": False,
            "is_deterministic": True,
            "input": [DENSE, SIGNED_DATA, UNSIGNED_DATA],
            "output": [PREDICTIONS],
        }

    @staticmethod
    def get_hyperparameter_search_space(
        feat_type: Optional[FEAT_TYPE_TYPE] = None, dataset_properties=None
    ):
        """
        Return the hyperparameter search space for the classifier.

        Args:
        - feat_type (Optional): Feature type. Defaults to None.
        - dataset_properties: Dataset properties. Defaults to None.

        Returns:
        - ConfigurationSpace: Hyperparameter search space.
        """
        cs = ConfigurationSpace()
        n_trees = UniformIntegerHyperparameter(
            name="n_trees", lower=100, upper=1000, default_value=100
        )
        n_estimators = UniformIntegerHyperparameter(
            name="n_estimators", lower=1, upper=6, default_value=1
        )
        bin_type = CategoricalHyperparameter(
            name="bin_type",
            choices=["percentile", "interval"],
            default_value="percentile"
        )
        criterion = CategoricalHyperparameter(
            name="criterion", choices=["gini", "entropy"],
            default_value="gini"
        )
        use_predictor = CategoricalHyperparameter(
            name="use_predictor", choices=[True, False],
            default_value=True
        )
        predictor = CategoricalHyperparameter(
            name="predictor", choices=["forest", "lightgbm", "xboost"],
            default_value="forest"
        )
        cs.add_hyperparameters(
            [
                n_trees,
                n_estimators,
                bin_type,
                criterion,
                use_predictor,
                predictor,
            ]
        )
        return cs
