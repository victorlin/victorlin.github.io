---
layout: post-no-cover
title: Creating an AWS Lambda Layer using CloudShell
date: 2021-2-15
description: 
ext_img: https://d1.awsstatic.com/serverless/Lambda%20Resources%20images/lambda_resources_3.299d6a5901be6ec9ffb72321716d25f7813c2319.png
tags: [software]
---

Using python packages from `pip` is a bit nontrivial on AWS Lambda. The solution is to use Lambda Layers, which act like virtual environments. Creating a layer programatically isn't straightforward, but it can be done.

A layer can be created by zipping packages downloaded from `pip`, but they must be compiled for use on Amazon Linux. One simple way to do that without spinning up an EC2 instance is with AWS CloudShell.

First, `virtualenv` must be installed on the CloudShell environment.

```sh
sudo pip install virtualenv
```

Without `sudo`, `pip install` yields an error `PermissionError: [Errno 13] Permission denied: '/usr/local/lib64/python3.7/site-packages/...'`. [Not sure why](https://dev.to/kojiisd/play-with-aws-cloudshell-5ba8).

It's also a good idea to set `alias pip=pip3`. Somehow this isn't the default on CloudShell.

Given a file `requirements.txt`, the script below can be run on CloudShell to produce a `layer.zip` file that is sufficient for Python 3.7, the installed Python version on CloudShell at the time of writing.

```sh
virtualenv ve
source ve/bin/activate
pip install -r requirements.txt
mkdir -p tmp/python
cp -rp ve/lib/python3.7/site-packages/* tmp/python
cp -rp ve/lib64/python3.7/site-packages/* tmp/python
pushd tmp
pushd python
rm -r *.dist-info *.virtualenv
popd
zip -r9 -q ../layer.zip python
popd
rm -r tmp ve
```