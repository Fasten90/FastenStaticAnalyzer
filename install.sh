#!/bin/bash
set -e

echo "Download pycparser"
DIR=pycparser
if [ -d "$DIR" ]; then
    cd $DIR && git fetch && cd ..
else
    git clone https://github.com/eliben/pycparser.git
fi

#echo "Create Python ENV"
#python -m venv venv

echo "Install requirements"
pip install -r requirements.txt
