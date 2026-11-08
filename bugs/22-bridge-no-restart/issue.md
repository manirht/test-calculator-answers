# After the Python helper dies, every statistics call fails until calc is restarted

In a long `calc serve` session the Python helper got killed (out-of-memory killer on my laptop). From then on:

```
> mean(1,2,3)
error[EXTERNAL]: write to python failed: Broken pipe (os error 32)
> mean(1,2,3)
error[EXTERNAL]: write to python failed: Broken pipe (os error 32)
```

and so on forever. Plain arithmetic keeps working. The first failure is understandable; the engine used to start a fresh
helper for the next call and everything carried on. Now only restarting the whole session helps.
