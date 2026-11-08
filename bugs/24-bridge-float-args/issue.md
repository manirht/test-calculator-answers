# mean(1/3, 1/3, 1/3) is not exactly 1/3

Arithmetic in this calculator is exact (`1/3 * 3` is exactly `1`) and the Python statistics are exact too, but once a
fraction goes through a statistics function it comes back slightly off:

```
$ calc eval "mean(1/3, 1/3, 1/3)" --places 15
0.333333333333
$ calc eval "mean(1/3, 1/3, 1/3) * 3" --places 15
0.999999999999
```

The mean of three identical values must be that value, and times 3 it must be exactly 1. With whole-number inputs
everything is fine, it's only when an argument is a fraction. The Python code itself looks exact when I call it directly
with `"1/3"` strings.
