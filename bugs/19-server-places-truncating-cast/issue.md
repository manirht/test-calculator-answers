# An enormous places value is accepted and treated as a small one

The server is supposed to refuse more than 30 decimal places (`places must be at most 30`) and it does for 31, 100 and a
million. But some values slip through:

```
{"id": 1, "expr": "1/3", "places": 4294967298}
-> {"id": 1, "ok": true, "value": "0.33", ...}
```

`4294967298` is nowhere near 30 yet it is accepted and I get two decimal places. It looks like the number wraps around:
4294967298 is 2^32 + 2. I found this while fuzzing the protocol with large numbers, so it's an input validation problem
rather than something a real client would send.
