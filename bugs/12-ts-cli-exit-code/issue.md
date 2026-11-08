# calc-ui exits with status 0 when the expression fails

In a script I rely on the exit status:

```
$ calc-ui "1/0"
error[DIV_BY_ZERO]: division by zero
$ echo $?
0
```

The error goes to stderr, which is right, but the status is `0`, so `calc-ui "1/0" || handle_error` never fires. The plain
`calc eval "1/0"` binary exits with `1` in the same situation. I expect `calc-ui` to do the same.
