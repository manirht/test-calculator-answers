# The constant e is wrong after the 13th decimal place

```
$ calc eval e --places 14
2.7182818284595
```

Euler's number is 2.718281828459045..., so to 14 places I expect `2.71828182845905`. The first twelve digits are right and then
it drifts, which I only noticed because I compared against a reference.

(`pi` looks fine.)
