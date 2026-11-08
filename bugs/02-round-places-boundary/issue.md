# round(x, 20) is rejected even though the message says 0 to 20

```
$ calc eval "round(1/3, 20)"
error[DOMAIN]: round places must be between 0 and 20
```

20 is between 0 and 20, so I would expect this to work. `round(1/3, 19)` is fine and `round(1/3, 21)` fails with the same
message, which makes sense. Only the boundary value is wrong.
