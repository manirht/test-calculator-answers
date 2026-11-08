# calc-ui --places 0 is rejected

I want whole numbers only, so I run:

```
$ calc-ui --places 0 "10/4"
calc-ui: --places needs a non-negative integer
```

Zero is a non-negative integer, and `:places 0` inside the REPL works fine. `--places 1` through `--places 30` are accepted.
Expected output for the command above is `3` (half-up).
