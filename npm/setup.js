const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");

const packageJson = require("./package.json");
const version = packageJson.version;
const vsix = path.join(__dirname, `slay-lang-${version}.vsix`);
const extensionId = "undefined_publisher.slay-lang";

function commandExists(cmd) {
    try {
        const check = process.platform === 'win32' ? `where ${cmd}` : `which ${cmd}`;
        execSync(check, { stdio: "ignore" });
        return true;
    } catch {
        return false;
    }
}

function installExtension() {
    console.log("\n✨ Setting up SlayLang...\n");

    if (!fs.existsSync(vsix)) {
        console.log("⚠️  VS Code extension not found.");
        console.log(`   Expected: ${vsix}`);
        return;
    }

    let vscode = null;
    if (commandExists("code")) vscode = "code";
    else if (commandExists("codium")) vscode = "codium";

    if (!vscode) {
        console.log("⚠️  VS Code/VSCodium not found.");
        return;
    }

    try {
        const installed = execSync(`${vscode} --list-extensions`, { encoding: "utf8" });
        if (installed.includes(extensionId)) {
            console.log("✅ SlayLang extension already installed.");
            return;
        }

        console.log("Installing SlayLang VS Code extension...");
        execSync(`${vscode} --install-extension "${vsix}"`, { stdio: "inherit" });
        console.log("✅ SlayLang extension installed!");
    } catch (err) {
        console.log("⚠️  Could not install extension automatically.");
        console.log(`   Install manually: code --install-extension "${vsix}"`);
    }
}

installExtension();