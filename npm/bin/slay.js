#!/usr/bin/env node

const { execFileSync } = require('child_process');
const path = require('path');

const args = process.argv.slice(2);

if (args.length === 0) {
    console.error("usage: slay <file.slay>");
    console.error("       slay setup   → install VS Code extension");
    process.exit(1);
}

if (args[0] === 'setup') {
    require('../setup.js');
    process.exit(0);
}

const isWindows = process.platform === 'win32';
const pythonCmd = isWindows ? 'python' : 'python3';
const interpreterPath = path.join(__dirname, '..', 'src', 'slay.py');

try {
    execFileSync(pythonCmd, [interpreterPath, ...args], { stdio: 'inherit' });
} catch (e) {
    process.exit(1);
}