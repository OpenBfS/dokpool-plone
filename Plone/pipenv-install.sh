#!/bin/sh

pipenv install setuptools==65.4.1
pipenv install
pipenv run buildout -v -c buildout_jenkins.cfg
