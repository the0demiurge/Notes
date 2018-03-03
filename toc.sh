#!/bin/sh
#python3 ./gitbook-auto-summary.py . -o
book sm -i node_modules
cd ..
tree Notes --dirsfirst -I '__pycache__|node_modules|*.png|*.gif|_book'
