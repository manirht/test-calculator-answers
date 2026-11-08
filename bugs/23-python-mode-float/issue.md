# mode() loses exactness: mode(1/3, 1/3, 1/2) * 3 is not 1

Everything else in the statistics functions is exact (`mean(1/3, 1/3, 1/3) * 3` is exactly `1`), but `mode` isn't:

```
$ calc eval "mode(1/3, 1/3, 1/2)" --places 12
0.333333333333
$ calc eval "mode(1/3, 1/3, 1/2) * 3" --places 12
0.999999999999
```

I expected `0.333333333333` times 3 to be exactly 1 because the mode is the value `1/3`, not an approximation of it. For
whole numbers `mode` is fine, which is why it took me a while to notice.
