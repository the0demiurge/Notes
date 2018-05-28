#!/bin/bash
#python3 ./gitbook-auto-summary.py . -o
book sm -i node_modules
cd ..
cat Notes/HEADER.md|tee Notes/README.md
echo "\`\`\`" |tee -a Notes/README.md
tree Notes --dirsfirst -I '__pycache__|node_modules|*.png|*.gif|_book|*.json|*.jpg'|tee -a Notes/README.md
echo "\`\`\`" |tee -a Notes/README.md
cd Notes

if [ ! -z $1 ];then
    if [ ! -d books ];then mkdir books;fi
    gitbook pdf . books/CharlesNotes.pdf
    gitbook epub . books/CharlesNotes.epub
    gitbook mobi . books/CharlesNotes.mobi
    gitbook build
    cp -r books _book
fi