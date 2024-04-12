# COMPSCI 235 Assignment 2

## Description

This project was created during my time at the University of Auckland. I have shared it here to demonstrate some of my knowledge with Python, SQL and Flask.

## Python version

Please use Python version 3.9 or newer versions for development. Some files use type hinting of `list` without importing typing.List, as in 3.9 this is no longer required. Also, some of the depending libraries of our web application do not support Python versions below 3.6!

## Installation

**Installation via requirements.txt**

```shell
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

## Testing with the pytest unit tests

Run `python -m pytest tests` to run all the tests.

## Execution of the web application

**Running the Flask application**

From the project directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

## Data sources 

The data in the excerpt files were downloaded from (Comic & Graphic):
https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home

On this webpage, you can find more books and authors in the same file format as in our excerpt, for example for different book genres. 
These might be useful to extend your web application with more functionality.

We would like to acknowledge the authors of these papers for collecting the datasets by extracting them from Goodreads:

*Mengting Wan, Julian McAuley, "Item Recommendation on Monotonic Behavior Chains", in RecSys'18.*

*Mengting Wan, Rishabh Misra, Ndapa Nakashole, Julian McAuley, "Fine-Grained Spoiler Detection from Large-Scale Review Corpora", in ACL'19.*
