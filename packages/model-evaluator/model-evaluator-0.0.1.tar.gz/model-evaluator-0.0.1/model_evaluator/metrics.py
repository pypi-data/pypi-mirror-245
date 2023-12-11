from abc import abstractmethod

from sklearn.metrics import (accuracy_score, balanced_accuracy_score, roc_auc_score, f1_score, precision_score,
                             recall_score)
from torch import Tensor


class Metric:
    __metric_name__ = ''

    @abstractmethod
    def evaluate(self, probabilities: Tensor,
                 predicted_labels: Tensor,
                 actual_labels: Tensor) -> float:
        pass


class Accuracy(Metric):
    __metric_name__ = 'Accuracy'

    def evaluate(self, probabilities: Tensor, predicted_labels: Tensor, actual_labels: Tensor) -> float:
        return accuracy_score(y_true=actual_labels, y_pred=predicted_labels)


class BalancedAccuracy(Metric):
    __metric_name__ = 'Balanced accuracy'

    def evaluate(self, probabilities: Tensor, predicted_labels: Tensor, actual_labels: Tensor) -> float:
        return balanced_accuracy_score(y_true=actual_labels, y_pred=predicted_labels)


class ROCAUC(Metric):
    __metric_name__ = 'ROC AUC'

    def evaluate(self, probabilities: Tensor, predicted_labels: Tensor, actual_labels: Tensor) -> float:
        return roc_auc_score(y_true=actual_labels, y_pred=probabilities)


class F1Score(Metric):
    __metric_name__ = 'F1 Score'

    def __init__(self, average='macro'):
        self._average = average

    def evaluate(self, probabilities: Tensor, predicted_labels: Tensor, actual_labels: Tensor) -> float:
        return f1_score(y_true=actual_labels, y_pred=predicted_labels, average=self._average)


class Precision(Metric):
    __metric_name__ = 'Precision'

    def evaluate(self, probabilities: Tensor, predicted_labels: Tensor, actual_labels: Tensor) -> float:
        return precision_score(y_true=actual_labels, y_pred=predicted_labels, average=self)


class Recall(Metric):
    __metric_name__ = 'Recall'

    def __init__(self, average='macro'):
        self._average = average

    def evaluate(self, probabilities: Tensor, predicted_labels: Tensor, actual_labels: Tensor) -> float:
        return recall_score(y_true=actual_labels, y_pred=predicted_labels, average=self._average)
