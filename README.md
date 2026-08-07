<p align="center">

**The programming language with attitude.**

[![npm version](https://img.shields.io/npm/v/slaylang.svg)](https://www.npmjs.com/package/slaylang)
[![npm downloads](https://img.shields.io/npm/dm/slaylang.svg)](https://www.npmjs.com/package/slaylang)
[![license](https://img.shields.io/npm/l/slaylang.svg)](https://github.com/FaizeenHoque/SlayLang/blob/main/LICENSE)
[![made with chaos](https://img.shields.io/badge/made%20with-chaos-ff69b4)](https://github.com/FaizeenHoque/SlayLang)

</p>

```
spin (vibe x = 10; x >= 0; x -= 1) {
    yap("nonsense")
}
```

---

## Install

### Quick install

```bash
npm install -g slaylang
slay setup
```

### Linux (Arch/Manjaro/etc.)

```bash
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
```

```bash
export PATH="$HOME/.npm-global/bin:$PATH"
```

```fish
fish_add_path ~/.npm-global/bin
```

### Run it

```bash
slay program.slay
```

---

## Why this exists

```
Exception: buddy, variable x does NOT exist
```

---

## Language tour

### Variables

```
vibe x = 10            # mutable variable
lockedin y = 42        # constant, don't even try to reassign it
vibe name = "slay"
vibe nothing = ghosted # null
```

| SlayLang | Meaning |
|---|---|
| `vibe` | mutable variable (`let`) |
| `lockedin` | constant (`const`) |
| `ghosted` | null / None |

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
yap(nocap)              # prints: nocap
yap(ghosted)            # prints: ghosted
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
vibe age = intify(snoop("how old are you? "))
vibe price = floatify(snoop("enter price: "))
```

| SlayLang | Meaning |
|---|---|
| `snoop(prompt)` | read input from stdin |
| `intify(value)` | convert to integer |
| `floatify(value)` | convert to float |

---

### Operators

```
vibe a = 2 ** 8      # power → 256
vibe b = 10 % 3      # modulo → 1
vibe c = 17 \ 5      # floor divide → 3
vibe d = a + b       # → 257
```

| SlayLang | Meaning |
|---|---|
| `+` `-` `*` `/` | standard arithmetic |
| `**` | power / exponent |
| `%` | modulo |
| `\` | floor divide |
| `==` `!=` `>` `<` `>=` `<=` | comparison |
| `&&` | logical and |
| `\|\|` | logical or |
| `nah` | logical not |

---

### Compound assignment

```
vibe x = 10
x += 5    # x is now 15
x -= 3    # x is now 12
x *= 2    # x is now 24
x /= 4    # x is now 6
```

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
    x -= 1
}

# for loop
spin (vibe i = 0; i <= 10; i += 1) {
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

```
cook factorial(n) {
    sus (n <= 1) {
        yeet 1
    }
    yeet n * factorial(n - 1)
}

yap(factorial(10))
```

| SlayLang | Meaning |
|---|---|
| `cook` | define a function |
| `yeet` | return a value |

---

### Arrays

```
vibe nums[] = [1, 2, 3, 4, 5]

yap(nums[0])       # 1
nums[0] = 99       # mutation
yap(nums[0])       # 99

# nested arrays
vibe matrix[] = [[1, 2], [3, 4]]
yap(matrix[0][1])  # 2
matrix[1][0] = 99
```

```
vibe arr[] = []
push(arr, 10)      # append
push(arr, 20)
pop(arr)           # remove last
yap(len(arr))      # 1
```

| SlayLang | Meaning |
|---|---|
| `push(arr, val)` | append to array |
| `pop(arr)` | remove last element |
| `len(arr)` | length of array |

---

### Full example

```
cook fizzbuzz(n) {
    spin (vibe i = 1; i <= n; i += 1) {
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

`slay setup` grabs the VS Code extension automatically. No marketplace digging.

---

## Contributing

Bug, infinite loop, fan taking off. Open an issue or send a PR. Real parser/lexer/evaluator, not a toy. Read the code first.

---

## License

MIT. Use it, fork it, break it. Just credit it.

---

<sub>Built by [Faizeen Hoque](https://github.com/FaizeenHoque).</sub>
