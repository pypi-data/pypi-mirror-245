# Model Evaluator


## Description

A package for training and evaluating PyTorch models.

Now it supports only visualization of training of models, but in future will support training 
and evaluation of many models which can be very useful for students.

If you have any bugs/improvement ideas, create an issue thread.

[GitHub repository](https://github.com/artemgalyan/model-evaluator)

[PyPi](https://pypi.org/project/model-evaluator/)

## Installation

For installation you need to execute following command:

    pip install model-evaluator

Then you can import library and use it in your code:

    import model_evaluator

## Example usage

    from model_evaluator import Trainer, PlottingOptions, Accuracy, F1Score

    train_data_loader = ...
    test_data_loader = ...
    model = ...
    optimizer = ...
    criterion = ... # those are yours

    trainer = Trainer(model, optimizer, criterion, [Accuracy(), F1Score()],
                      plotting_options=PlottingOptions.PLOT_BOTH, plot_interval=8)
    trainer.train(NUM_EPOCHS, train_data_loader, test_data_loader, device)

## Authors

Artsiom Halian - [GitHub](github.com/artyomgalyan)

## Versions

1.0.0 - Initial version