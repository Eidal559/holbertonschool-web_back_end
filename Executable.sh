#!/bin/bash

read -p "Enter the name of the file: " file
read -p "Enter the commit message: " message

git add "$file"
git update-index --chmod=+x "$file"
git ls-files --stage
git commit -m "$message"
git push
