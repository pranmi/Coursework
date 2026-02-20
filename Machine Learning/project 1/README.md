# Data Processing (datasetProcessing.py)
All processing of the data is handled in datasetProcessing.py
Upon running it will prompt for which dataset and representation type (must enter integers)
It will return both the train and test csv's for your chosen set/type in the csv folder
These csv's are also already in the csv folder

# Learning Algorithms (ModelTraining.py)
Similar to the processing, run and it will prompt for a dataset, representation type, and model type
It will exit early if you choose incompatible types (bernoulli model on multinomial rep or vice versa)
After making choices, it will run through both the training of the model and prediction before printing the report statistics to console and exiting
Additionally, if logistic regression was chosen, it will print which lambda was chosen.
Learning rate and iterations for LR are hard coded into the function call on line 39 as the 3rd and 4th input variables respectively
iterations is set relatively high, (5000), running in about 30 seconds on my machine. May need to be tuned down

There is no AI transcript file as I didn't use any AI for this project, mainly just looked up pandas and numpy stuff on stack overflow to help with implimentation