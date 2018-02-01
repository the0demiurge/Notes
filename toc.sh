#!/bin/sh
python3 ./gitbook-auto-summary.py . -o
cd ..
tree Notes --dirsfirst -I '__pycache__'
