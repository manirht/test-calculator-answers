# A too-large --places is accepted, then every expression fails

I fat-fingered `--places 300`:

```
$ calc-ui --places 300
> 1+1
error[BAD_REQUEST]: places must be at most 30
> 2+2
error[BAD_REQUEST]: places must be at most 30
```

The session starts as if everything were fine and then every line fails. The command line should refuse the value up front,
the same way it refuses `--places -1`: `calc-ui: --places must be at most 30`.
