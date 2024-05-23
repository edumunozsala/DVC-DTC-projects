
from sklearn.metrics import f1_score, classification_report, accuracy_score, confusion_matrix


import os
import yaml
import pickle
from scipy import sparse

def load_datasets(params):

    # Load the features for the train and test dataset
    X_test = sparse.load_npz(params['X_test'])
    
    # Load the labels for the train and test dataset
    with open(params['y_test'], "rb") as fp:   # Unpickling
        y_test = pickle.load(fp)

    return X_test, y_test

def load_model(params):
    # Load model and data.
    with open(params['model_path'], "rb") as fd:
        model = pickle.load(fd)
    print("Model loaded successfully:", model)
    
    return model

def evaluate_model(params):
    # Load data
    X_test, y_test = load_datasets(params)

    # Load the model
    model= load_model(params)
    
    # Get the predictions
    predictions = model.predict(X_test)

    # Evaluate model
    f1_score= f1_score(y_test, predictions, average='macro')
    acc=  accuracy_score(y_test, predictions)
    cm = confusion_matrix(y_test, predictions)
    print(f'Test Accuracy: {acc}')
    print(f'F1 score: {f1_score}')

