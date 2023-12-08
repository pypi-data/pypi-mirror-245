# typora-git-uploader

## Table of Contents
  * [Installation](#installation)
  * [Usage](#Usage)
  * [Quick start](#quick-start)
  * [Features](#features)
  
## Installation

Download using pip via pypi.

```bash
$ pip install typora-git-uploader
```

or 

Download using git.

```bash
$ git clone https://github.com/TyrantLucifer/typora-upload.git
$ cd typora-git-uploader
$ python setup.py install
```

## Usage

```bash
$ typora-git-uploader -h
usage: typora-git-uploader [-h] [--username USERNAME] [--repo REPO] [--token TOKEN] [--branch BRANCH] [--upload remote_upload_dir local_uploaded_path]
options:
  -h, --help            show this help message and exit
  --username USERNAME   github username
  --repo REPO           github repo expected to be uploaded
  --token TOKEN         github token required to upload
  --branch BRANCH       github repo branch expected to be uploaded
  --upload remote_upload_dir local_uploaded_path
                        remote_upload_dir and local_uploaded_path
```

## Quick start

```bash
$ typora-git-uploader 
      --username=USERNAME --repo=REPOSITORY --token=API_TOKEN 
      --branch=BRANCH --upload EXPECTED_REMOTE_PATH LOCAL_UPLOADED_PATH     
```

## Features

  * `Typora` Plugins for Uploading Files to Git