## Getting started

### Project

## Register datasets

1.First we initialize DVC
```bash
dvc init --subdir
```
```bash
dvc init --subdir
```
2. Download the initial dataset for our project.
It's a dataset from Hugging Face Hub containing texts in Spanish and a predictioned label "baised" or "non-biased".
We execute the script `download_raw_data` to read the dataset, get the columns we are interested in and then save it to a CSV file.
```bash
python -m downloadraw_data
```
The destination path is defined in the `params.yaml` file.

Now, in the data directory `data` there is our initial dataset.

3. Now, we register the data in DVC.

```bash
dvc add data/raw/twitter-genderbias.csv
```

4. Now we include the .gitignore and .dvc data file in git
```bash
git add data/raw/.gitignore data/raw/twitter-genderbias.csv.dvc
```

Let's commit the changes.

5. Now, we can add S3 as remote storage to DVC:
```bash
dvc remote add -d myremote s3://dvc-project-week/project/
```

6. And we save our DVC files to the remote storage
```bash
dvc push
```
7. Modify the `twitter-genderbias.csv` and add it to dvc track
```bash
dvc add data/raw/twitter-genderbias.csv
```
7. Commit changes to Git
```bash
git add .
git commit -m "project: update initial dataset"
```
8. Rollback to a previuos version of the data file

First we need to get the previous commit and run git checkout to that commit:

```bash
git log
git checkout <commit_id>
```
9. Now, twitter-genderbias.csv.dvc is pointing to the previous version but not twitter-genderbias.csv. To restore the file we need to run a dvc checkuot:
```bash
dvc checkout
```

10. Get back to the last commit:
```bash
git checkout main
dvc checkout
```

And then we process our dataset to get a featurized dataset and we track the files with dvc
```bash
dvc add data/processed/*
```
And register dvc files in git.
```bash
git add data/processed/y_test.pkl.dvc data/processed/X_test.npz.dvc data/processed/y_train.pkl.dvc data/processed/.gitignore data/processed/X_train.npz.dvc
```
We commit the changes to git and save the dvc cache to the remote storage

11. Save changes to remote storage
```bash
dvc push
```

## Configure S3 as Remote storage

First we need to install awscli using conda or pip

awscli

and we also need the library dvc-s3:
```bash
pip install dvc-s3
```

Then we configure the `awscli` credentials:

```bash
aws configure
```

the create a bucket in S3:
```bash
aws s3api create-bucket \
    --bucket dvc-project-week \
    --region us-east-1
```

Now, we canm add S3 as remote storage:
```bash
dvc remote add -d myremote s3://dvc-project-week/project/
```

## Create a DVC Pipeline

The pipeline consists of 4 stages:
1. Download the initial dataset

```bash
dvc stage add -n download_data --force \
                -p data_source,raw_data_path,raw_filename \
                -d scripts/download_raw_data.py \
                -o data/pipeline/raw \
                python scripts/download_raw_data.py
```

2. Process and featurized the dataset
```bash
dvc stage add -n process_data --force \
                -p raw_data_path,raw_filename,test_size,processed_data_path \
                -d scripts/process_data.py -d data/pipeline/raw \
                -o data/pipeline/processed \
                python scripts/process_data.py
```

3. Train a Logistic Regression Model
```bash
dvc stage add -n train --force \
                -p processed_data_path,max_iters,C,random_state,model_path \
                -d scripts/train.py -d data/pipeline/processed \
                -o model/model.pkl \
                python scripts/train.py
```

4. Evaluate the model
```bash
dvc stage add -n evaluation --force \
                -p processed_data_path,model_path \
                -d scripts/evaluation.py -d data/pipeline/processed -d model/model.pkl \
                python scripts/evaluation.py
```

Our final pipeline DAG looks like this:
![Pipeline DAG](images/dvc-dag.png)


Once defined we include the new dvc files in git
```bash
git add dvc.yaml data/pipeline/.gitignore
```

Now we can run the pipeline:
```bash
dvc repro
```

And save the DVC cache to the remote storage:
```bash
dvc push
```