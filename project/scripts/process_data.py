from datasets import load_dataset, Dataset
import spacy
from bs4 import BeautifulSoup
import re
import os

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.pipeline import Pipeline

from scipy import sparse
import pickle
import yaml

class LinguisticPreprocessor(BaseEstimator, TransformerMixin):
    """
    Preprocesador lingüístico para limpieza y normalización de texto, incluida la eliminación de stopwords.

    Attributes
    ----------
    nlp : spacy.language.Language
        Instancia de spaCy para el procesamiento del lenguaje.
    stopwords : set
        Conjunto de stopwords.
    """
    def __init__(self, nlp, remove_html=True, lemmatize_stopwords=True):
        self.nlp = nlp
        self.stopwords = nlp.Defaults.stop_words
        self.remove_html = remove_html
        self.lemmatize_stopwords= lemmatize_stopwords


    def remove_html_tags(self, text):
        """
        Elimina las etiquetas HTML del texto.

        Parameters
        ----------
        text : str
            Texto a limpiar.

        Returns
        -------
        str
            Texto sin etiquetas HTML.
        """
        return BeautifulSoup(text, "html.parser").get_text()

    def lemmatize_and_remove_stopwords(self, doc):
        """
        Lematiza el documento y elimina las stopwords.

        Parameters
        ----------
        doc : spacy.tokens.doc.Doc
            Documento procesado por spaCy.

        Returns
        -------
        str
            Texto lematizado sin stopwords.
        """
        return " ".join([token.lemma_ for token in doc if not token.is_punct and token.text.lower() not in self.stopwords])

    def fit(self, X, y=None):
        """
        Método de ajuste requerido por scikit-learn TransformerMixin. No se realiza ningún ajuste.

        Parameters
        ----------
        X : iterable
            Textos a preprocesar.
        y : None
            Ignorado.

        Returns
        -------
        self
        """
        return self

    def transform(self, X, y=None):
        """
        Transforma los textos aplicando limpieza, eliminación de HTML, lematización y eliminación de stopwords.

        Parameters
        ----------
        X : iterable
            Textos a preprocesar.

        Returns
        -------
        list
            Lista de textos preprocesados.
        """
        transformed_X = []
        for text in X:
            if self.remove_html:
              text = self.remove_html_tags(text)

            text = re.sub(r'\s+', ' ', text).strip()  # Elimina espacios extras
            doc = self.nlp(text)
            if self.lemmatize_stopwords:
              transformed_text = self.lemmatize_and_remove_stopwords(doc)
            else:
              transformed_text = text

            transformed_X.append(transformed_text)
        return transformed_X

def preprocess_label(sample: dict) -> dict:
    """
    Preprocesa la información de etiquetas de un diccionario de muestra.

    Parámetros
    ----------
    sample : dict
        Diccionario de entrada que contiene información de predicción.

    Devuelve
    -------
    dict
        Diccionario procesado con la información de la etiqueta extraída y almacenada bajo la clave "label".
    """
    sample["label"] = sample["prediction"][0]["label"]
    sample["label"] = 1 if sample["label"] == "biased" else 0
    return sample
    
def load_datasets_csv(params):
    #dataset = load_dataset(params['data_source'], split='train')
    dataset = Dataset.from_csv(params['raw_data_path'], header=0)
    dataset = dataset.train_test_split(test_size=params['test_size'], seed=42)
    
    return dataset

    
if __name__ == "__main__":
    # Load parameters
    with open('params.yaml') as f:
        params = yaml.safe_load(f)
    # Leemos el dataset
    dataset = load_datasets_csv(params)
    print('Num examples: ', len(dataset))
    # Need to run
    # ! python -m spacy download es_core_news_sm
    # Transform the label to binary
    #dataset = dataset.map(preprocess_label)
    # Load the spacey Language model
    nlp = spacy.load("es_core_news_sm")
    # Instanciar el preprocesador
    preprocessor = LinguisticPreprocessor(nlp)

    # Crear el pipeline
    pipeline = Pipeline([
        ('preprocess', preprocessor),
        ('vectorizer', TfidfVectorizer()),
    ])

    # Preparar los datos
    X_train = dataset["train"]["text"]
    X_test = dataset["test"]['text']

    # Entrenar el modelo
    X_train_transformed = pipeline.fit_transform(X_train)
    X_test_transformed = pipeline.transform(X_test)

    # Extract the labels for train and test
    y_train = dataset["train"]["label"]
    y_test = dataset["test"]["label"]
    
    # Save the X train and test sparse matrix
    sparse.save_npz(os.path.join(params['processed_data_path'], "X_train.npz"), X_train_transformed)
    sparse.save_npz(os.path.join(params['processed_data_path'], "X_test.npz"), X_test_transformed)
    #sparse.save_npz("X_test.npz", X_test_transformed)
    
    # Save the labels
    with open(os.path.join(params['processed_data_path'], "y_train.pkl"), "wb") as fp:   #Pickling
        pickle.dump(y_train, fp)
    with open(os.path.join(params['processed_data_path'], "y_test.pkl"), "wb") as fp:   #Pickling
        pickle.dump(y_test, fp)

