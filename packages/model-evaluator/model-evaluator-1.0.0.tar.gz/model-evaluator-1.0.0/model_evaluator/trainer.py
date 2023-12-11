from enum import Enum
from math import ceil
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from IPython.display import clear_output, HTML, display
from torch import Tensor
from torch.nn import Module
from torch.nn.modules.loss import _Loss
from torch.optim import Optimizer
from torch.utils.data import DataLoader

from .metrics import Metric


class PlottingOptions(Enum):
    """
    Enumeration of plotting options.
    NO_PLOT - doesn't show any plots
    PLOT_ONLY_TRAIN - plots only train losses
    PLOT_ONLY_TEST - plots only test losses
    PLOT_BOTH - plots both train and test losses
    """
    NO_PLOT = 'no'
    PLOT_ONLY_TRAIN = 'train_only'
    PLOT_ONLY_TEST = 'test_only'
    PLOT_BOTH = 'both'


class Plotter:
    """
    Class responsible for plotting losses
    """

    def __init__(self,
                 plot_options: PlottingOptions,
                 *,
                 train_line: str = 'solid',
                 test_line: str = 'dashed'):
        """
        :param plot_options: determines what to show on the plot
        :param train_line: line style for train loss
        :param test_line: line style for test loss

        For line styles refer to https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
        """
        self._train_line = train_line
        self._test_line = test_line
        self._plot_options = plot_options
        self._train_history: list[float] = [0.]
        self._test_history: list[float] = [0.]
        self._batches_count = 1

    def set_batches_count(self, batches_count: int) -> None:
        """
        Sets the expected number of batches
        """
        self._batches_count = batches_count

    def add_train_loss(self, train_loss: float) -> None:
        self._train_history.append(train_loss)

    def add_test_loss(self, test_loss: float) -> None:
        self._test_history.append(test_loss)

    def replot(self) -> None:
        """
        Plots the data
        """
        if self._plot_options in [PlottingOptions.PLOT_ONLY_TRAIN, PlottingOptions.PLOT_BOTH]:
            plt.plot(
                np.linspace(0, len(self._train_history) / self._batches_count, len(self._train_history)),
                self._train_history,
                linestyle=self._train_line,
                label='Train Loss')
        if self._plot_options in [PlottingOptions.PLOT_ONLY_TEST, PlottingOptions.PLOT_BOTH]:
            plt.plot(
                np.linspace(0, len(self._test_history), len(self._test_history)),
                self._test_history,
                linestyle=self._test_line,
                label='Test Loss')
        if self._plot_options != PlottingOptions.NO_PLOT:
            plt.legend()
            plt.xlabel('Epochs')
            plt.ylabel('Loss')
            plt.show()


class Trainer:
    def __init__(self,
                 model: Module,
                 optimizer: Optimizer,
                 loss: _Loss,  # base class for some reason is protected
                 metrics: list[Metric],
                 *,
                 plotting_options: PlottingOptions = PlottingOptions.NO_PLOT,
                 save_models: bool = True,
                 plot_interval: int = 4,
                 save_path: Path = Path('.'),
                 train_line_style: str = 'solid',
                 test_line_style: str = 'dashed') -> None:
        """
        :param model: model to train
        :param optimizer: optimizer for model
        :param loss: loss function for model, expects to have mean reduction (for plotting concerns)
        :param metrics: metrics to compute after every epoch
        :param plotting_options: plotting options, defaults to PlottingOptions.NO_PLOT
        :param save_models: whether to save model after every epoch, defaults to True
        :param plot_interval: the frequency of plotting (in terms of batches), defaults to 4
        :param save_path: path to save models, defaults to Path('.')
        :param train_line_style: line style of train loss
        :param test_line_style: line style of test loss

        For line styles refer to https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
        """
        self._model = model
        self._optimizer = optimizer
        self._loss = loss
        self._metrics = metrics
        self._save_models = save_models
        self._plotter = Plotter(plotting_options, train_line=train_line_style, test_line=test_line_style)
        self._plot_interval = plot_interval
        self._test_metrics_history: dict[str, list[float]] = {metric.__metric_name__: [] for metric in metrics}
        self._test_metrics_history['loss'] = []
        self._train_losses = []
        self._save_path = save_path

        df_columns = ['Epoch', 'Training Loss', 'Test Loss']
        for metric in self._metrics:
            df_columns.append(metric.__metric_name__)
        self._history = pd.DataFrame(columns=df_columns)
        self._history.index = self._history['Epoch']
        self._history = self._history.drop('Epoch', axis=1)

    def train(self, epochs: int,
              train_loader: DataLoader,
              test_loader: DataLoader,
              device: torch.device) -> None:
        """
        Trains the model for given number of epochs
        :param epochs: number of epochs to train the model
        :param train_loader: train data
        :param test_loader: test data
        :param device: device to train the model on
        :return: None
        """
        plotting_count = int(ceil(len(train_loader) / self._plot_interval))
        self._plotter.set_batches_count(plotting_count)
        self._model.train()

        plotted_loss = 0
        plot_counter = 0
        for epoch in range(epochs):
            # base training loop
            train_loss = 0

            for i, data in enumerate(train_loader):
                inputs, labels = data
                inputs = inputs.to(device)
                labels = labels.to(device)

                self._optimizer.zero_grad()

                outputs = self._model(inputs)
                if outputs.shape[1] == 1:  # binary classification
                    outputs = outputs.view(-1)
                loss = self._loss(outputs, labels.float())
                loss.backward()
                self._optimizer.step()
                plotted_loss += loss.item()
                plot_counter += 1
                if plot_counter % self._plot_interval == 0:
                    self._plotter.add_train_loss(plotted_loss / plot_counter)
                    plotted_loss = 0
                    plot_counter = 0
                    self._show()
                train_loss += loss.item()
            if self._save_models:
                torch.save(self._model.state_dict(), str(self._save_path / f'model_{epoch}'))

            # evaluating the model
            self._model.eval()
            result = [epoch + 1, train_loss]
            with torch.no_grad():
                predictions, labels = self._evaluate(test_loader, device)
                predictions = predictions.cpu()
                labels = labels.cpu()
                if predictions.shape[1] == 1:  # binary classification
                    predictions = predictions.view(-1)
                    classes = predictions >= 0.5
                else:
                    classes = predictions.argmax(dim=1)
                test_loss = self._loss(predictions, labels)
                self._plotter.add_test_loss(test_loss.item())
                result.append(test_loss.item())
                for metric in self._metrics:
                    result.append(metric.evaluate(predictions, classes, labels))
            self._history.loc[len(self._history)] = result
            self._show()

    def history(self) -> pd.DataFrame:
        return self._history

    def _evaluate(self, data_loader: DataLoader, device: torch.device) -> tuple[Tensor, Tensor]:
        """
        Evaluate the model on the provided data
        :param data_loader: data to evaluate model on
        :param device: device to evaluate on
        :return: tuple of predictions and actual labels
        """
        result_preds = []
        result_labels = []
        for data in data_loader:
            inputs, labels = data
            inputs = inputs.to(device)
            labels = labels.to(device)
            result_preds.append(self._model(inputs))
            result_labels.append(labels.float())
        return torch.cat(result_preds), torch.cat(result_labels)

    def _show(self) -> None:
        """
        Plots the data (graph and metrics history)
        """
        clear_output(wait=True)
        self._plotter.replot()
        display(HTML(self._history.to_html()))
