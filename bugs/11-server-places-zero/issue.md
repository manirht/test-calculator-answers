# :places 0 has no effect in the REPL

In the interactive session:

```
> :places 0
places = 0
> 10/4
2.5
```

I would expect `3` (half-up, zero decimal places). `:places 2` and `:places 5` work as expected, and the echoed
setting says `places = 0`, so the REPL believes it is set. Starting with `calc-ui --places 0` doesn't help either.
`calc eval "10/4" --places 0` on its own prints `3`, so the engine can do it.
