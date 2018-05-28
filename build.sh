#!/bin/bash
#python3 ./gitbook-auto-summary.py . -o
book sm -i node_modules

cat HEADER|tee README.md
echo "\`\`\`" |tee -a README.md
echo "Notes" |tee -a README.md
tree --dirsfirst -I '__pycache__|node_modules|*.png|*.gif|_book|*.json|*.jpg'|grep -v '^\.$'|tee -a README.md
echo "\`\`\`" |tee -a README.md

if [ ! -z $1 ];then
    if [ ! -d books ];then mkdir books;fi
    gitbook build
    gitbook pdf . books/CharlesNotes.pdf
    gitbook epub . books/CharlesNotes.epub
    gitbook mobi . books/CharlesNotes.mobi
    cp -r books _book
    rm _book/.gitignore
fi
echo 'OK'