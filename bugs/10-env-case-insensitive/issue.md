# Variable names are not case-sensitive

The README says variable names are case-sensitive. They are not:

```
> Rate = 5
5
> rate * 2
10
> RATE = 7
7
> Rate
7
```

`rate`, `Rate` and `RATE` are all the same variable. I use `T` for time and `t` for temperature in the same session
and they overwrite each other. Expected: `rate` should be an unknown variable after only `Rate` was assigned.
