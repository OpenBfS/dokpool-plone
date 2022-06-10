#!/bin/sh

pipenv install setuptools==62.0.0
pipenv install
pipenv run buildout -v -c buildout_jenkins.cfg
