# pvariance() is reported as an unknown function

```
$ calc eval "pvariance(2,4,4,4,5,5,7,9)"
error[UNKNOWN_FUNC]: unknown function 'pvariance'
$ calc eval "variance(2,4,4,4,5,5,7,9)"
4.5714285714
$ calc eval "pstddev(2,4,4,4,5,5,7,9)"
2
```

The population variance function is in the Python package (I can call it directly) and the other statistics functions work
through `calc`. It's also missing from tab completion in `calc-ui`.
