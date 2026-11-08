# pv() at a 0% rate returns a single payment

```
$ calc eval "pv(0, 12, 100)"
100
```

Twelve payments of 100 with no interest are worth 1200 today, not 100. With any non-zero rate the result is right
(`pv(1/100, 12, 100)` is fine) and `pmt` and `fv` handle a zero rate correctly. It's only `pv`.
