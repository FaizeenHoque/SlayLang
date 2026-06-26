const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");

const version = require("./package.json").version;

const vsix = path.join(
    __dirname,
    `slay-lang-${version}.vsix`
);

console.log("\n✨ Setting up SlayLang...\n");


if (!fs.existsSync(vsix)) {
    console.log("⚠️ VS Code extension file not found.");
    console.log("Install it manually from:");
    console.log(vsix);
    process.exit(0);
}


function commandExists(cmd) {
    try {
        execSync(`which ${cmd}`, { stdio: "ignore" });
        return true;
    } catch {
        return false;
    }
}


let vscode = null;

if (commandExists("code")) {
    vscode = "code";
}
else if (commandExists("codium")) {
    vscode = "codium";
}


if (!vscode) {
    console.log("⚠️ VS Code not detected.");
    console.log("Install the extension manually:");
    console.log(vsix);
    process.exit(0);
}


try {
    console.log("Installing SlayLang VS Code extension...");

    execSync(
        `${vscode} --install-extension "${vsix}"`,
        {
            stdio: "inherit"
        }
    );

    console.log("✅ SlayLang extension installed!");

} catch (err) {
    console.log("⚠️ Could not automatically install extension.");
    console.log("Install manually:");
    console.log(vsix);
}