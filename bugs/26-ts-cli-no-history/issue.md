# --no-history still writes the history file

I use `calc-ui --no-history` when I'm calculating things I'd rather not keep (salaries, mostly):

```
$ echo "85000 / 12
:quit" | calc-ui --no-history
7083.3333333333
$ cat .calc_history.json
[
  {
    "expr": "85000 / 12",
    ...
```

The flag clearly prevents history from being *read* at start (my old entries don't come back) but the new entries are still
saved at the end of the session. The help text says "do not read or write history".
