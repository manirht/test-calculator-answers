# pmt() is off by one in the 12th decimal place

```
$ calc eval "pmt(5/1200, 360, 200000)" --places 12
1073.643246024277
```

My reference calculator (arbitrary precision) says `1073.643246024278`. The difference is always in the last kept
digit and always downwards, never upwards: I compared a dozen results and the engine's number is never larger than the
reference. With the default 10 places you can't see it, you have to ask for 12.
