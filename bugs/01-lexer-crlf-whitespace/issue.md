# Multi-line expressions fail with "unexpected character"

I keep long formulas in shell scripts and wrap them over several lines so they stay readable:

```sh
calc eval "1000 *
  (1 + 0.05)"
```

This used to work. Now it fails:

```
error[SYNTAX]: unexpected character '
' at 6
```

The same thing happens with expressions copied out of a Windows text file (the line ends with a carriage return).
A line break should be treated like a space.
