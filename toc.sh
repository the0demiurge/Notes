#!/bin/sh
#python3 ./gitbook-auto-summary.py . -o
book sm -i node_modules
cd ..
echo "\`\`\`" |tee Notes/README.md
tree Notes --dirsfirst -I '__pycache__|node_modules|*.png|*.gif|_book'|tee -a Notes/README.md
echo "\`\`\`" |tee -a Notes/README.md
