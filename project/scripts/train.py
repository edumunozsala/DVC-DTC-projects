from sklearn.linear_model import SGDClassifier, LogisticRegression

import os
import yaml
import pickle
from scipy import sparse

def load_datasets(params):

    # Load the features for the train and test dataset
    X_train = sparse.load_npz(params['X_train'])
    X_test = sparse.load_npz(params['X_test'])
    
    # Load the labels for the train and test dataset
    with open(params['y_train'], "rb") as fp:   # Unpickling
        y_train = pickle.load(fp)
    with open(params['y_test'], "rb") as fp:   # Unpickling
        y_test = pickle.load(fp)

    return X_train, X_test, y_train, y_test

def train_model(params):

    # Load data
    X_train, X_test, y_train, y_test = load_datasets(params)

    # Train model
    #model = SGDClassifier(max_iter=1000, tol=1e-3, class_weight="balanced", random_state=42)
    model= LogisticRegression(max_iter=params['max_iters'], tol=1e-3, C=params['C'], 
                              class_weight="balanced", random_state=params['random_state'])
    
    model.fit(X_train, y_train)

    # Save the model
    model_directory = 'model'
    
    if not os.path.exists(model_directory):
        os.makedirs(model_directory)
    
    with open(params['model_path'], 'wb') as f:
        pickle.dump(model, f)
    
    print(f'Model saved to {params['model_path']}')

    # Evaluate model
    score = model.score(X_test, y_test)
    print(f'Test Accuracy: {score}')

if __name__=="__main__":
    # Load parameters
    with open('params.yaml') as f:
        params = yaml.safe_load(f)

    train_model(params)