# Adding to the largest integer gives a negative number

```
$ calc eval "170141183460469231731687303715884105727 + 2"
-170141183460469231731687303715884105726
```

I know there is a limit on how big numbers can get (multiplying two huge numbers reports `OVERFLOW`, which is fine), but this one
returns a *wrong number* instead of an error, which is much worse than failing. `... + 1` correctly reports `OVERFLOW`; adding
2 or more doesn't. Same for subtracting from the most negative number.
