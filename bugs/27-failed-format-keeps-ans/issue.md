# A line that fails with OVERFLOW still replaces ans

```
> :places 30
> 5
5
> 123456789012/7
error[OVERFLOW]: arithmetic overflow
> ans
17636684144.857142857142857142857142857
```

When a line fails, the previous result should stay in `ans` (that's what happens for `1/0`: `ans` is still `5` afterwards).
Here the line reports an error but `ans` has silently changed to the value of the failed line, which I never saw.
The error comes from printing with 30 places; the computation itself was fine.
