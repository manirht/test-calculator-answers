# lcm() returns a negative number when an argument is negative

```
$ calc eval "lcm(-4, 6)"
-12
$ calc eval "lcm(4, -6)"
-12
$ calc eval "lcm(-4, -6)"
12
```

A least common multiple is never negative. `lcm(4, 6)` is `12` as it should be, and `gcd(-12, 18)` correctly gives `6`.
I would expect `12` in all three cases above.
