# Floating point precision loss: 1/3 prints only 10 digits

```
$ calc eval "1/3"
0.3333333333
```

A proper calculator shows at least 15 digits (`0.333333333333333`). It looks like this engine uses 32-bit floats internally and
loses precision. This is a serious accuracy problem for financial calculations, please fix the arithmetic to use
higher precision.
