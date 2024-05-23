# DVC-DTC-projects
Testing and developing ML projects using DVC in the DataTalkClub experience

## Why DVC?

Even with all the success we've seen in machine learning, especially with deep learning and its applications in business, data scientists still lack best practices for organizing their projects and collaborating effectively. This is a critical challenge: while ML algorithms and methods are no longer tribal knowledge, they are still difficult to develop, reuse, and manage.

### Basic uses of DVC

If you store and process data files or datasets to produce other data or machine learning models, and you want to:

- track and save data and machine learning models the same way you capture code;
- create and switch between versions of data and ML models easily;
- understand how datasets and ML artifacts were built in the first place;
- compare model metrics among experiments;
- adopt engineering tools and best practices in data science projects;

*Data Version Control (DVC)* lets you capture the versions of your data and models in Git commits, while storing them on-premises or in cloud storage. It also provides a mechanism to switch between these different data contents. The result is a single history for data, code, and ML models that you can traverse — a proper journal of your work!

DVC enables data versioning through codification. You produce simple metafiles once, describing what datasets, ML artifacts, etc. to track. This metadata can be put in Git in lieu of large files. Now you can use DVC to create snapshots of the data, restore previous versions, reproduce experiments, record evolving metrics, and more!

## Installation

You can folow the guidelines in the [official documentation](https://dvc.org/doc/install)

### In a Linux machine

We first recommend to create a virtual enviroment using pipenv or conda depending on your python installation.

Then you can just install DVC as a python library

```bash
pip install dvc
```
The check the version installed:

```bash
dvc --version
```

In my case I installed version 3.50.2

## Getting started

Our first experiment wil consists in a demo with the initial steps: create a data file and keep track of its version usinf dvc and git. 
Then we'll connect dvc to a remote storage in S3 to save our DVC cache.

You can follow the step-by-step initial demo in this [file](./basic-demo/README.md)




