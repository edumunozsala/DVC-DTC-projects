## Getting started

### Demo: Basic usage

1. Create a subfolder `step-demo` for this demo
2. Create a data folder `data`
3. Create a `data.txt`:
```text
First version
```
4.Initialize DVC
```bash
dvc init --subdir
```
5. Add `data.txt` to tracking:
```bash
dvc add data/data.txt
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
