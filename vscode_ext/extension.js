const vscode = require('vscode');

function activate(context) {
    const provider = vscode.languages.registerCompletionItemProvider('slay', {
        provideCompletionItems() {
            const items = [];

            const keywords = ['sus', 'mid', 'tho', 'grind', 'spin', 'dip', 'skip', 'yeet', 'cook'];
            const declarations = ['vibe', 'lockedin'];
            const booleans = ['nocap', 'cap', 'ghosted'];
            const builtins = ['yap', 'rant', 'snoop', 'numify'];

            keywords.forEach(k => {
                const item = new vscode.CompletionItem(k, vscode.CompletionItemKind.Keyword);
                item.detail = 'keyword';
                items.push(item);
            });

            declarations.forEach(k => {
                const item = new vscode.CompletionItem(k, vscode.CompletionItemKind.Keyword);
                item.detail = 'declaration';
                items.push(item);
            });

            booleans.forEach(k => {
                const item = new vscode.CompletionItem(k, vscode.CompletionItemKind.Value);
                item.detail = 'boolean';
                items.push(item);
            });

            builtins.forEach(k => {
                const item = new vscode.CompletionItem(k, vscode.CompletionItemKind.Function);
                item.detail = 'builtin function';
                item.insertText = new vscode.SnippetString(`${k}($1)`);
                items.push(item);
            });

            return items;
        }
    });

    context.subscriptions.push(provider);
}

function deactivate() {}

module.exports = { activate, deactivate };