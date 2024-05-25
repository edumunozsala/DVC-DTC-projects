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

Now, we register the data in DVC.

```bash
dvc add data/raw/twitter-genderbias.csv
```

Now we include the .
```bash
git add data/raw/.gitignore data/raw/twitter-genderbias.csv.dvc
```

Let's commit the changes.

Now, we canm add S3 as remote storage:
```bash
dvc remote add -d myremote s3://dvc-project-week/project/
```

And we save our DVC files to the remote storage
```bash
dvc push
```

DVC performs the following action:

- Adds the data/data.txt path to data/.gitignore to ensure that the data file is not tracked by Git but by DVC instead.
- Generates a .dvc file (e.g., data/data.txt.dvc), which contains metadata about the data file such as its MD5 hash, size, and relative path.
- Stores a copy of the data file in the DVC cache located in the .dvc/cache directory. This cached file serves as a reference and is identified by a hash value derived from the file’s content, rather than creating a duplicate of the original file

6. Modify the `data.txt` and add it to dvc track
```bash
dvc add data/data.txt
```
7. Commit changes to Git
```bash
git add .
git commit -m "basic demo: update data.txt"
```
8. Modify the data.txt file, add to dvc tracking and commit changes

Once the file has changed run:

```bash
dvc add data/data.txt
git add .
git commit -m "basic demo: update data.txt"
```
9. Rollback to a previuos version of the data file

First we need to get the previous commit and run git checkout to that commit:

```bash
git log
git checkout <commit_id>
```
Now, data.txt.dvc is pointing to the previous version but not data.txt. To restore the file we need to run a dvc checkuot:
```bash
dvc checkout
```

10. Get back to the last commit:
```bash
git checkout main
dvc checkout
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
dvc remote add -d myremote s3://dvc-project-week/tests/
```

Now, let's test it. We create a new data file `data_s3.txt` and add it to dvc tracking

```bash
dvc add data/data_s3.txt 
```

Commit the changes to Git
```bash
git add .
```

Finally we can push the DVC cache to the S3 location:
```bash
dvc push
```
