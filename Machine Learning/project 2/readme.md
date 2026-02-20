All code for the first part of the project (everything but the MNIST performance) is done in project2.py
Run, and you will be prompted for the clause count, then number of datapoints, then which model
Then it will run with these parameters, tune the hyperparameters on validation, andrun the final model to predict
**Warning** Gradient boost takes a full minute or two on the largest datasets

project2part2.py is for the MNIST dataset.
It is pretty much identical, except I hard coded the hyperparameters found for the largest datasets in part one (for most, a few I let reset to the default or gradient boost criteria where I couldn't use exponential)
as such I commented out the hyperparameter tuning methods and restructured the methods to directly take the dataframe inputs
Will just prompt for which model and run, then return the accuracy
Note: I had to set the number of estimators for gradient boost on the mnist set very low as run time was exceedingly long otherwise.