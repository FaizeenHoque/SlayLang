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

That's a `for` loop. It counts down, prints `"nonsense"` eleven times, and does it *with style*.

---

## Install

### Quick install

```bash
npm install -g slaylang
slay setup
```

`slay setup` drops the **VS Code extension** in automatically — syntax highlighting included, no extra clicks.

### Linux (Arch/Manjaro/etc.)

If you installed Node via pacman, set a user npm prefix first to avoid needing sudo:

```bash
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
```

Add to your shell config:

```bash
# bash/zsh — add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.npm-global/bin:$PATH"
```

```fish
# fish — add to ~/.config/fish/config.fish
fish_add_path ~/.npm-global/bin
```

Restart your terminal, then run the quick install above.

### Run it

```bash
slay program.slay
```

---

## Why SlayLang exists

Nobody asked for this. That's exactly why it had to be built.

- 🔥 **Readable-ish syntax.** `vibe` instead of `let`. `yap` instead of `print`. You'll get used to it, or you won't, and that's also valid.
- ⚙️ **A real lexer, parser, and evaluator under the hood** — not a regex hack pretending to be a compiler.
- 🪞 **Error messages with personality.** SlayLang doesn't fail quietly:

```
Exception: buddy, variable x does NOT exist
```

You will be informed. You will be slightly judged. You will fix your code.

---

## Language tour

### Variables

```
vibe x = 10          # mutable variable
lockedin y = 42      # constant — don't even try to reassign it
vibe name = "slay"
vibe nothing = ghosted   # null
```

| SlayLang | Meaning |
|---|---|
| `vibe` | mutable variable (`let`) |
| `lockedin` | constant (`const`) |
| `ghosted` | null |

---

### Booleans

```
vibe isReal = nocap    # true
vibe isCap = cap       # false
```

| SlayLang | Meaning |
|---|---|
| `nocap` | `true` |
| `cap` | `false` |

---

### Printing

```
yap("hello world")      # prints: hello world
rant("hello world")     # prints: hello world !!
```

| SlayLang | Meaning |
|---|---|
| `yap(...)` | print normally |
| `rant(...)` | print with `!!` at the end |

---

### Input & type conversion

```
vibe name = snoop("what's your name? ")
vibe age = numify(snoop("how old are you? "))
```

| SlayLang | Meaning |
|---|---|
| `snoop(prompt)` | read input from stdin |
| `numify(value)` | convert string to number |

---

### Operators

```
vibe a = 2 ** 8      # power → 256
vibe b = 10 % 3      # modulo → 1
vibe c = a + b       # → 257
```

| SlayLang | Meaning |
|---|---|
| `+` `-` `*` `/` | standard arithmetic |
| `**` | power / exponent |
| `%` | modulo |
| `==` `!=` `>` `<` `>=` `<=` | comparison |

---

### Conditionals

```
sus (x > 10) {
    yap("big number")
} mid (x == 10) {
    yap("exactly ten")
} tho {
    yap("small number")
}
```

| SlayLang | Meaning |
|---|---|
| `sus` | `if` |
| `mid` | `else if` |
| `tho` | `else` |

---

### Loops

```
# while loop
grind (x > 0) {
    yap(x)
    x = x - 1
}

# for loop
spin (vibe i = 0; i <= 10; i = i + 1) {
    sus (i == 5) { skip }   # continue
    sus (i == 8) { dip }    # break
    yap(i)
}
```

| SlayLang | Meaning |
|---|---|
| `grind` | `while` loop |
| `spin` | `for` loop |
| `dip` | `break` |
| `skip` | `continue` |

---

### Functions

```
cook greet(name) {
    yeet name
}

yap(greet("world"))
```

| SlayLang | Meaning |
|---|---|
| `cook` | define a function |
| `yeet` | return a value |

> Functions only have access to their own parameters — they don't see outer variables. Pass everything in as arguments.

---

### Full example

```
cook fizzbuzz(n) {
    spin (vibe i = 1; i <= n; i = i + 1) {
        sus (i % 15 == 0) {
            yap("FizzBuzz")
        } mid (i % 3 == 0) {
            yap("Fizz")
        } mid (i % 5 == 0) {
            yap("Buzz")
        } tho {
            yap(i)
        }
    }
}

fizzbuzz(20)
```

---

## Editor support

Run `slay setup` after installing to automatically install the **SlayLang VS Code extension** — syntax highlighting for `.slay` files out of the box

---

## Contributing

Found a bug? Hit an infinite loop? Made the fan spin up? [Open an issue](https://github.com/FaizeenHoque/SlayLang/issues) or send a PR. Read the code first — it's a real parser/lexer/evaluator, treat it like one.

---

## License

MIT. Use it, fork it, roast it. Just don't pretend you wrote it.

---

<sub>Built by [Faizeen Hoque](https://github.com/FaizeenHoque). SlayLang has strong opinions about your variable names.</sub>