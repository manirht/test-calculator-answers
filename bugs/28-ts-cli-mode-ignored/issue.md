# calc-ui --mode is ignored

```
$ calc eval 2/3 --places 2 --mode truncate
0.66
$ calc-ui --places 2 --mode truncate 2/3
0.67
```

The engine's own CLI honours `--mode`. `calc-ui` accepts the flag (a typo in it is reported) and `--places` works, but the result is
still rounded half-up. Typing `:mode truncate` inside an interactive session works, so the REPL itself is fine.
