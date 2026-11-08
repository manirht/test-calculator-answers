# 2^3 is wrong: it should be 1 (XOR), not 8

```
$ calc eval "2^3"
8
```

In every programming language I use, `^` is bitwise XOR, so `2^3` is `1`. The calculator gives `8`. This is a bug in the
operator: please make `^` XOR, and add `**` for exponentiation if people need it.
