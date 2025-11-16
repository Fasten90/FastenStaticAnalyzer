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

python3 -m pip install -r requirements.txt --break-system-packages

