#!/bin/bash
set -e

# sanity checks
if ! command -v vsce &> /dev/null; then
    echo "✗ vsce not found. Run: npm install -g @vscode/vsce"
    exit 1
fi

read -p "change version to: " VERSION
read -p "commit message (default: release v$VERSION): " COMMIT_MESSAGE

COMMIT_MESSAGE=${COMMIT_MESSAGE:-"release v$VERSION"}

echo "→ updating versions..."
sed -i "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" npm/package.json
sed -i "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" vscode_ext/package.json

echo "→ packaging VS Code extension..."
cd vscode_ext
vsce package --out slay-lang-$VERSION.vsix
cd ..

echo "→ copying vsix to npm/..."
cp vscode_ext/slay-lang-$VERSION.vsix npm/slay-lang-$VERSION.vsix

echo "→ removing old vsix files..."
find npm -name "slay-lang-*.vsix" ! -name "slay-lang-$VERSION.vsix" -delete

echo "→ syncing src/ into npm/..."
rm -rf npm/src
cp -r src npm/src

echo "→ publishing to npm..."
cd npm
npm publish
cd ..

echo "→ cleaning up..."
rm -rf npm/src
rm -f npm/slay-lang-$VERSION.vsix
rm -f vscode_ext/slay-lang-$VERSION.vsix

echo "→ tagging release..."
git add -A
git commit -m "$COMMIT_MESSAGE"
git tag v$VERSION
git push && git push --tags

echo "✓ slaylang@$VERSION shipped"