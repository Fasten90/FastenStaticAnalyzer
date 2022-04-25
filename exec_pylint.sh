#!/bin/bash
set -e

pylint --disable=R,C,W FastenStaticAnalyzer.py 

pylint --exit-zero FastenStaticAnalyzer.py 
