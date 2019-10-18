#!/bin/bash

ver=$1
env_name=$2
pyenv install $ver
pyenv virtualenv $1 $2