from abc import abstractmethod

from sklearn.metrics import (accuracy_score, balanced_accuracy_score, roc_auc_score, f1_score, precision_score,
                             recall_score)
from torch import Tensor


class Metric:
    """
    Base class for all metrics
    """
    __metric_name__ = ''

    @abstractmethod
    def evaluate(self, probabilities: Tensor,
                 predicted_labels: Tensor,
                 actual_labels: Tensor) -> float:
        """
        :param probabilities: probability of classes
        :param predicted_labels: predicted labels, i.e. argmax(probabilities, dim=-1)
        :param actual_labels: actual labels
        :return: computed metric
        If binary classification is used, all arrays are expected to have (n,) shape
        """
        pass


class Accuracy(Metric):
    """
    Computes accuracy score
    It is a wrapper for sklearn.metrics.accuracy_score

    Read: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html
    """
    __metric_name__ = 'Accuracy'

    def evaluate(self, probabilities: Tensor, predicted_labels: Tensor, actual_labels: Tensor) -> float:
        return accuracy_score(y_true=actual_labels, y_pred=predicted_labels)


class BalancedAccuracy(Metric):
    """
    Computes balanced accuracy score
    It is a wrapper for sklearn.metrics.balanced_accuracy_score

    Read: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.balanced_accuracy_score.html
    """
    __metric_name__ = 'Balanced accuracy'

    def evaluate(self, probabilities: Tensor, predicted_labels: Tensor, actual_labels: Tensor) -> float:
        return balanced_accuracy_score(y_true=actual_labels, y_pred=predicted_labels)


class ROCAUC(Metric):
    """
    Computes ROC-AUC score
    It is a wrapper for sklearn.metrics.roc_auc_score

    Read: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html
    """
    __metric_name__ = 'ROC AUC'

    def evaluate(self, probabilities: Tensor, predicted_labels: Tensor, actual_labels: Tensor) -> float:
        return roc_auc_score(y_true=actual_labels, y_score=probabilities)


class F1Score(Metric):
    """
    Computes F1 score
    It is a wrapper for sklearn.metrics.f1_score

    Read: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html
    """
    __metric_name__ = 'F1 Score'

    def __init__(self, average='binary') -> None:
        """

        :param average: This parameter is required for multiclass/multilabel targets.
        If None, the scores for each class are returned.
        Otherwise, this determines the type of averaging performed on the data.

        Read more: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html
        """
        self._average = average

    def evaluate(self, probabilities: Tensor, predicted_labels: Tensor, actual_labels: Tensor) -> float:
        return f1_score(y_true=actual_labels, y_pred=predicted_labels, average=self._average)


class Precision(Metric):
    """
    Computes precision metric
    It is a wrapper for sklearn.metrics.precision_score

    Read: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html
    """
    __metric_name__ = 'Precision'

    def __init__(self, average: str = 'binary') -> None:
        """

        :param average: This parameter is required for multiclass/multilabel targets.
        If None, the scores for each class are returned.
        Otherwise, this determines the type of averaging performed on the data

        Read more: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html
        """
        self._average = average

    def evaluate(self, probabilities: Tensor, predicted_labels: Tensor, actual_labels: Tensor) -> float:
        return precision_score(y_true=actual_labels, y_pred=predicted_labels, average=self._average)


class Recall(Metric):
    """
    Computes recall metric
    It is a wrapper for sklearn.metrics.recall_score

    Read: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html
    """
    __metric_name__ = 'Recall'

    def __init__(self, average='binary') -> None:
        """

        :param average: This parameter is required for multiclass/multilabel targets.
        If None, the scores for each class are returned.
        Otherwise, this determines the type of averaging performed on the data

        Read more: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html
        """
        self._average = average

    def evaluate(self, probabilities: Tensor, predicted_labels: Tensor, actual_labels: Tensor) -> float:
        return recall_score(y_true=actual_labels, y_pred=predicted_labels, average=self._average)
