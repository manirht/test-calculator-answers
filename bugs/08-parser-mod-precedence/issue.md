# % has the wrong precedence: 2 + 7 % 4 gives 1

```
$ calc eval "2 + 7 % 4"
1
```

I expected `5`: modulo should bind like `*` and `/`, so this is `2 + (7 % 4)` = `2 + 3`. It looks like the addition happens first,
`(2 + 7) % 4` = `1`. `2 + 7 * 4` and `2 + 7 / 4` are both fine.

Parenthesised versions work, which is why I only noticed it in a longer formula.
