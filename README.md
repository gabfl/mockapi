# mockapi

[![Build Status](https://travis-ci.org/gabfl/mockapi.svg?branch=master)](https://travis-ci.org/gabfl/mockapi)
[![codecov](https://codecov.io/gh/gabfl/mockapi/branch/master/graph/badge.svg)](https://codecov.io/gh/gabfl/mockapi)
[![MIT licensed](https://img.shields.io/badge/license-MIT-green.svg)](https://raw.githubusercontent.com/gabfl/mockapi/master/LICENSE)

Simple Python tool to mock API responses

## What is MockApi?

MockAPI is a Python program allowing you to start a Flask webserver to create a mock API in matter of seconds.

You can provide any payload you would like (Json, XML or text/html) and MockAPI will create a unique URL that will return the given payload.

![Demo](img/demo.gif?raw=true)

## Installation

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
# export FLASK_ENV=development
export FLASK_APP=src/app.py
flask run
```