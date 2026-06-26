# SlayLang 💅⚡

**The programming language with attitude.**

[![npm version](https://img.shields.io/npm/v/slaylang.svg)](https://www.npmjs.com/package/slaylang)
[![npm downloads](https://img.shields.io/npm/dm/slaylang.svg)](https://www.npmjs.com/package/slaylang)
[![license](https://img.shields.io/npm/l/slaylang.svg)](https://github.com/FaizeenHoque/SlayLang/blob/main/LICENSE)
[![made with chaos](https://img.shields.io/badge/made%20with-chaos-ff69b4)](https://github.com/FaizeenHoque/SlayLang)

Most languages throw `NullPointerException`. SlayLang throws shade.

```
spin (vibe x = 10; x >= 0; x = x - 1) {
    yap("nonsense")
}
```

That's a `for` loop. It counts down, it prints `"nonsense"` eleven times, and it does it *with style*. No semicolons forgotten, no fan-spinning infinite loops (anymore) — just clean, unbothered execution.

---

## Install

```bash
npm install -g slaylang
```

That's it. One command, and it also drops the **VS Code extension** in for you automatically (syntax highlighting included, no extra clicks, no begging the marketplace).

Run it:

```bash
slay program.slay
```

---

## Why SlayLang exists

Nobody asked for this. That's exactly why it had to be built.

- 🔥 **Readable-ish syntax.** `vibe` instead of `let`. `yap` instead of `print`. You'll get used to it, or you won't, and that's also valid.
- ⚙️ **A real parser and evaluator under the hood** — not a regex hack pretending to be a compiler.
- 🪞 **Error messages with personality.** SlayLang doesn't fail quietly:

```
Exception: buddy, variable x does NOT exist
```

You will be informed. You will be slightly judged. You will fix your code.

---

## Language tour

| SlayLang | Does what | You'd normally write |
|---|---|---|
| `vibe x = 0` | declares a variable | `let x = 0` |
| `spin (vibe i = 0; i <= 10; i = i + 1) { ... }` | a C-style `for` loop | `for (let i = 0; i <= 10; i++) { ... }` |
| `yap("...")` | prints to stdout | `console.log("...")` |

> More keywords are landing as the language grows — this table reflects what's actually shipped, not what's planned. Check the [repo](https://github.com/FaizeenHoque/SlayLang) for the latest.

---

## Editor support

The npm install automatically packages and installs the official **SlayLang VS Code extension** — syntax highlighting for `.slay` files out of the box. If you're not on VS Code, or the auto-install fails silently (it's designed to fail quietly rather than break your install), grab the `.vsix` straight from the [repo](https://github.com/FaizeenHoque/SlayLang).

---

## Contributing

Found a bug? Hit an infinite loop? Made the fan spin up? [Open an issue](https://github.com/FaizeenHoque/SlayLang/issues) or send a PR. Read the code first — it's a real parser/lexer/evaluator, treat it like one.

---

## License

MIT. Use it, fork it, roast it. Just don't pretend you wrote it.

---

<sub>Built by [Faizeen Hoque](https://github.com/FaizeenHoque). SlayLang has strong opinions about your variable names.</sub>