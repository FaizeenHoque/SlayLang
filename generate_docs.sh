#!/bin/bash

files=$(find . -maxdepth 1 -name "*.py" | sort)

if [ -z "$files" ]; then
    echo "no .py files found here bestie 💀"
    exit 1
fi

echo "found:"
for f in $files; do
    echo "  $f"
done

python -m pdoc $files -o ./docs

echo "done! open ./docs to see your documentation"