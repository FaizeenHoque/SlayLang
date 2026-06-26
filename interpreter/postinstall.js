const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");

const packageJson = require("./package.json");

const version = packageJson.version;

const vsix = path.join(
    __dirname,
    `slay-lang-${version}.vsix`
);

const extensionId = "undefined_publisher.slay-lang";


function commandExists(cmd) {
    try {
        execSync(`which ${cmd}`, {
            stdio: "ignore"
        });
        return true;
    } catch {
        return false;
    }
}


function installExtension() {
    console.log("\n✨ Setting up SlayLang...\n");


    if (!fs.existsSync(vsix)) {
        console.log("⚠️ SlayLang VS Code extension not found.");
        console.log(`Expected: ${vsix}`);
        return;
    }


    let vscode = null;

    if (commandExists("code")) {
        vscode = "code";
    } else if (commandExists("codium")) {
        vscode = "codium";
    }


    if (!vscode) {
        console.log("⚠️ VS Code/VSCodium not found.");
        console.log("Install the extension manually:");
        console.log(vsix);
        return;
    }


    try {
        const installed = execSync(
            `${vscode} --list-extensions`,
            {
                encoding: "utf8"
            }
        );


        if (installed.includes(extensionId)) {
            console.log("✅ SlayLang extension already installed.");
            return;
        }


        console.log("Installing SlayLang VS Code extension...");


        execSync(
            `${vscode} --install-extension "${vsix}"`,
            {
                stdio: "inherit"
            }
        );


        console.log("✅ SlayLang extension installed!");

    } catch (err) {
        console.log("⚠️ Could not install SlayLang extension.");
        console.log("Install manually from:");
        console.log(vsix);
    }
}


installExtension();