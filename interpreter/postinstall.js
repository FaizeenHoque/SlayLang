const { execSync } = require('child_process');
const path = require('path');

const vsix = path.join(__dirname, 'slay-lang-0.1.2.vsix');

try {
    execSync(`code --install-extension ${vsix}`, { stdio: 'inherit' });
    console.log('SlayLang VS Code extension installed!');
} catch (e) {
    console.log('Could not install VS Code extension automatically. Install it manually from slay-lang-0.1.2.vsix');
}