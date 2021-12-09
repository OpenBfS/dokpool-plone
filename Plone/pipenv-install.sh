#!/bin/sh

pipenv install setuptools==42.0.0
pipenv install
pipenv run buildout -v -c buildout_jenkins.cfg
