# pv(-1, 3, 100) kills the Python helper

```
$ calc eval "pv(-1, 3, 100)"
error[EXTERNAL]: python process exited
```

A rate of -100% is nonsense but I'd expect a normal domain error like the one I get for -2 (`rate must be greater than -1`).
Instead the whole Python helper process dies. Running it again works only because the engine silently starts a new helper.
`fv(-1, 3, 100)` and `npv(-1, 10, 20)` behave the same way.
