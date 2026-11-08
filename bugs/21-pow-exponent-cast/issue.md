# 2^4294967297 returns 2 instead of an overflow error

Huge exponents are supposed to be rejected: `2^99999999999` correctly says `error[OVERFLOW]`. But if I go a bit higher:

```
$ calc eval "2^4294967297"
2
$ calc eval "2^4294967296"
1
```

`2^4294967297` is certainly not 2 and `2^4294967296` is certainly not 1. These look like the exponent is wrapping around:
4294967296 is 2^32. I'd expect `error[OVERFLOW]: exponent is too large` for both, as for the smaller huge exponent.
