# A long sum fails with TOO_DEEP

I generate formulas from a spreadsheet export. A sum with a couple of hundred terms fails:

```
$ calc eval "$(yes 1 | head -300 | paste -sd+ -)"
error[TOO_DEEP]: expression is nested too deeply
```

There is no nesting here at all, it's `1+1+1+...+1`. A 100 term sum works and so does any other long flat
expression up to a point, then it suddenly stops working. Deeply nested parentheses are *supposed* to be rejected, but this
isn't nested.
