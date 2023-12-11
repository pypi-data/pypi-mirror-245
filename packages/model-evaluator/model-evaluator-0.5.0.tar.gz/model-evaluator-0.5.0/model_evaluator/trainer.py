from enum import Enum
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
    NO_PLOT = 'no'
    PLOT_ONLY_TRAIN = 'train_only'
    PLOT_ONLY_TEST = 'test_only'
    PLOT_BOTH = 'both'


class Plotter:
    def __init__(self,
                 plot_options: PlottingOptions,
                 batch_size: int, *,
                 train_line: str = 'solid',
                 test_line: str = 'dashed'):
        self._train_line = train_line
        self._test_line = test_line
        self._plot_options = plot_options
        self._batch_size = batch_size
        self._train_history: list[float] = [0.]
        self._test_history: list[float] = [0.]

    def add_train_loss(self, train_loss: float) -> None:
        self._train_history.append(train_loss)

    def add_test_loss(self, test_loss: float) -> None:
        self._train_history.append(test_loss)

    def replot(self) -> None:
        if self._plot_options in [PlottingOptions.PLOT_ONLY_TRAIN, PlottingOptions.PLOT_BOTH] \
                and self._train_history:
            plt.plot(
                np.linspace(0, len(self._train_history) / self._batch_size, len(self._train_history)),
                self._train_history,
                linestyle=self._train_line,
                label='Train Loss')
        if self._plot_options in [PlottingOptions.PLOT_ONLY_TEST, PlottingOptions.PLOT_BOTH] \
                and self._test_history:
            plt.plot(
                np.linspace(0, len(self._test_history)),
                self._test_history,
                self._test_line,
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
                 batch_size: int = 64,
                 save_path: Path = Path('.')
                 ) -> None:
        self._model = model
        self._optimizer = optimizer
        self._loss = loss
        self._metrics = metrics
        self._save_models = save_models
        self._plotter = Plotter(plotting_options, batch_size * plot_interval)
        self._plot_interval = plot_interval
        self._test_metrics_history: dict[str, list[float]] = {metric.__metric_name__: [] for metric in metrics}
        self._test_metrics_history['loss'] = []
        self._train_losses = []
        self._save_path = save_path

        df_columns = ['Epoch', 'Training Loss', 'Test Loss']
        for metric in self._metrics:
            df_columns.append(metric.__metric_name__)
        self._history = pd.DataFrame(columns=df_columns)

    def train(self, epochs: int,
              train_loader: DataLoader,
              test_loader: DataLoader,
              device: torch.device) -> None:

        self._model.train()

        plotted_loss = 0
        plot_counter = 0
        for epoch in range(epochs):
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
            self._model.eval()
            result = [epoch + 1, train_loss]
            with torch.no_grad():
                predictions, labels = self._evaluate(test_loader, device)
                if predictions.shape[1] == 1:
                    predictions = predictions.view(-1)
                    classes = predictions >= 0.5
                else:
                    classes = predictions.argmax(dim=1)
                test_loss = self._loss(predictions, labels)
                self._plotter.add_test_loss(test_loss.item())
                result.append(test_loss.item())
                for metric in self._metrics:
                    result.append(metric.evaluate(predictions, classes, labels))
            self._history[-1] = result
            self._show()

    def _evaluate_metrics(self, data_loader: DataLoader,
                          state_dict: dict[str, list[float]],
                          save_losses: bool,
                          save_metrics: bool,
                          device: torch.device) -> None:
        if not save_losses and not save_metrics:
            return

        self._model.eval()
        with torch.no_grad():
            predictions, labels = self._evaluate(data_loader, device)
            if predictions.shape[1] == 1:
                predictions = predictions.view(-1)
                classes = predictions >= 0.5
            else:
                classes = predictions.argmax(dim=1)
            if save_losses:
                state_dict['loss'] = self._loss(predictions, labels.float())
            if save_metrics:
                for metric in self._metrics:
                    state_dict[metric.__metric_name__].append(metric.evaluate(predictions, classes, labels))

    def _evaluate(self, data_loader: DataLoader, device: torch.device) -> tuple[Tensor, Tensor]:
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
        clear_output(wait=True)
        self._plotter.replot()
        display(HTML(self._history.to_html()))
