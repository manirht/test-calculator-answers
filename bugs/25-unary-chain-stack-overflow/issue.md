# calc crashes (SIGSEGV) on a very long run of minus signs

Found while fuzzing the CLI with long inputs:

```
$ calc eval "$(printf -- '-%.0s' $(seq 1 200000))1"
Segmentation fault (core dumped)
```

Deeply nested parentheses are rejected cleanly (`error[TOO_DEEP]: expression is nested too deeply`), but the same amount of
nesting written as repeated unary minus takes the whole process down. In `calc serve` that kills the session, and anything
that feeds untrusted formulas to the server (a web form, a shared sheet) can crash it with one line.
