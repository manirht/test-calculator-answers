# irr() says it did not converge for an investment that loses money

```
$ calc eval "irr(-100, 50)"
error[DOMAIN]: irr did not converge
```

I put in 100 and got 50 back, so the return is -50% and there is a perfectly good answer. `irr(-100, 110)` gives `0.1`
as expected, and so do a few others with positive returns. It is only when the money comes back as less than was put in
that it gives up.
