#!/bin/bash
set -e

read -p "change version to: " VERSION

echo "→ updating versions..."

# update both package.json files
sed -i "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" interpreter/package.json
sed -i "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" vscode_ext/package.json


echo "→ packaging VS Code extension..."

cd vscode_ext
vsce package --out slay-lang-$VERSION.vsix
cd ..


echo "→ copying vsix to interpreter..."

cp vscode_ext/slay-lang-$VERSION.vsix interpreter/slay-lang-$VERSION.vsix


echo "→ removing old vsix files..."

find interpreter -name "slay-lang-*.vsix" ! -name "slay-lang-$VERSION.vsix" -delete


echo "→ publishing to npm..."

cd interpreter
npm publish
cd ..


echo "✓ slaylang@$VERSION shipped"