#!/usr/bin/env node

const { execFileSync } = require('child_process');
const path = require('path');

const args = process.argv.slice(2);

if (args.length === 0) {
    console.error("usage: slay <file.slay>");
    process.exit(1);
}

const interpreterPath = path.join(__dirname, '..', 'slay.py');

try {
    execFileSync('python3', [interpreterPath, ...args], {
        stdio: 'inherit'
    });
} catch (e) {
    process.exit(1);
}