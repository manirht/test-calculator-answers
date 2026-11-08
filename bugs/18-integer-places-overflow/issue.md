# Whole numbers fail with OVERFLOW when many decimal places are requested

```
$ calc eval 12345678901 --places 10
12345678901
$ calc eval 12345678901 --places 30
error[OVERFLOW]: arithmetic overflow
```

It's an integer, so there is nothing to round and it should print as is however many places I ask for. I only noticed
because a script passes `--places 30` for everything. Fractions with more than a few integer digits and 30 places
overflow too, but that I can understand, a whole number is a different matter.
