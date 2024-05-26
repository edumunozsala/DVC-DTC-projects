from datasets import load_dataset
import yaml

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
    
def load_datasets_hf(params):
    dataset = load_dataset(params['data_source'], split='train')
    #dataset = dataset.train_test_split(test_size=params['test_size'], seed=42)
    
    return dataset

    
if __name__ == "__main__":
    # Load parameters
    with open('params.yaml') as f:
        params = yaml.safe_load(f)
    
    dataset = load_datasets_hf(params)
    print('Num examples: ', len(dataset))
    
    #print(dataset['prediction']['label'])

    # Save the dataset to a csv file
    (
    dataset.to_pandas()
    .assign(label= lambda df: df['prediction'].map(lambda x: x[0]['label']))
    [['text','prediction','label']]
    ).to_csv(params['raw_data_path'], header=True, index=False)   
    #dataset.to_csv(params['raw_data_path'], header=True, index=False)
    #print("Save raw dataset to ",params['raw_data_path'])
        
