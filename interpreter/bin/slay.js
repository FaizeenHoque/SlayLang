#!/usr/bin/env node

const { execFileSync, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

function commandExists(cmd) {
    try {
        execSync(`which ${cmd}`, { stdio: 'ignore' });
        return true;
    } catch {
        return false;
    }
}

function installVSCodeExtension() {
    const version = require('../package.json').version;

    const vsix = path.join(
        __dirname,
        '..',
        `slay-lang-${version}.vsix`
    );

    if (!fs.existsSync(vsix)) {
        return;
    }

    let vscode = null;

    if (commandExists('code')) {
        vscode = 'code';
    } else if (commandExists('codium')) {
        vscode = 'codium';
    }

    if (!vscode) {
        return;
    }

    const extensionId = 'undefined_publisher.slay-lang';

    try {
        const installed = execSync(
            `${vscode} --list-extensions`,
            { encoding: 'utf8' }
        );

        if (installed.includes(extensionId)) {
            return;
        }

        console.log("✨ Installing SlayLang VS Code extension...");

        execSync(
            `${vscode} --install-extension "${vsix}"`,
            {
                stdio: 'inherit'
            }
        );

        console.log("✅ SlayLang extension installed!");

    } catch {
        console.log("⚠️ Could not install SlayLang extension.");
    }
}


const args = process.argv.slice(2);

if (args.length === 0 || !args[0].endsWith('.slay')) {
    console.error("bestie... that's not a .slay file");
    process.exit(1);
}


// only install extension when actually running Slay code
installVSCodeExtension();


const interpreterPath = path.join(
    __dirname,
    '..',
    'slay.py'
);

try {
    execFileSync(
        'python3',
        [interpreterPath, ...args],
        {
            stdio: 'inherit'
        }
    );
} catch (e) {
    process.exit(1);
}