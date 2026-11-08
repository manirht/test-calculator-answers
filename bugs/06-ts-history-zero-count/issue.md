# :history 0 says there is no history

```
> 1+1
2
> :history 0
(no history)
```

I had just evaluated something, so "(no history)" is misleading. `:history -1` and `:history x` print the usage hint
(`usage: :history [count]`); I would expect `:history 0` to do the same since a count of zero makes no sense.
