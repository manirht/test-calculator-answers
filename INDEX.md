# Bug index

32 bugs (none: 2, python: 5, rust: 19, ts: 6)

| id | lang | tier | category | kind | title |
|---|---|---|---|---|---|
| 01 | rust | L1 | lexer | fix | Multi-line expressions fail with "unexpected character" |
| 02 | rust | L1 | builtins | fix | round(x, 20) is rejected even though the message says 0 to 20 |
| 03 | rust | L1 | constants | fix | The constant e is wrong after the 13th decimal place |
| 04 | ts | L1 | cli-args | fix | calc-ui --places 0 is rejected |
| 05 | ts | L1 | cli-args | fix | A too-large --places is accepted, then every expression fails |
| 06 | ts | L1 | repl-commands | fix | :history 0 says there is no history |
| 07 | python | L1 | finance | fix | pv() at a 0% rate returns a single payment |
| 08 | rust | L2 | parser | fix | % has the wrong precedence: 2 + 7 % 4 gives 1 |
| 09 | rust | L2 | builtins | fix | lcm() returns a negative number when an argument is negative |
| 10 | rust | L2 | variables | fix | Variable names are not case-sensitive |
| 11 | rust (+ts) | L3 | server-protocol | fix | :places 0 has no effect in the REPL |
| 12 | ts (+rust) | L2 | cli | fix | calc-ui exits with status 0 when the expression fails |
| 13 | python (+rust) | L3 | finance | fix | pmt() is off by one in the 12th decimal place |
| 14 | python | L3 | finance | fix | irr() says it did not converge for an investment that loses money |
| 15 | rust | L3 | builtins | fix | sqrt(1/2) returns 1 |
| 16 | rust | L3 | parser | fix | A long sum fails with TOO_DEEP |
| 17 | rust | L3 | arithmetic | fix | Adding to the largest integer gives a negative number |
| 18 | rust | L3 | formatting | fix | Whole numbers fail with OVERFLOW when many decimal places are requested |
| 19 | rust | L3 | server-protocol | fix | An enormous places value is accepted and treated as a small one |
| 20 | python (+rust) | L3 | finance | fix | pv(-1, 3, 100) kills the Python helper |
| 21 | rust | L4 | arithmetic | fix | 2^4294967297 returns 2 instead of an overflow error |
| 22 | rust (+python) | L4 | python-bridge | fix | After the Python helper dies, every statistics call fails until calc is restarted |
| 23 | python (+rust) | L4 | stats | fix | mode() loses exactness: mode(1/3, 1/3, 1/2) * 3 is not 1 |
| 24 | rust (+python) | L5 | python-bridge | fix | mean(1/3, 1/3, 1/3) is not exactly 1/3 |
| 25 | rust | L6 | parser | fix | calc crashes (SIGSEGV) on a very long run of minus signs |
| 26 | ts (+rust) | L2 | cli | fix | --no-history still writes the history file |
| 27 | rust | L3 | session-state | fix | A line that fails with OVERFLOW still replaces ans |
| 28 | ts (+rust) | L2 | cli | fix | calc-ui --mode is ignored |
| 29 | rust (+python) | L2 | python-bridge | fix | pvariance() is reported as an unknown function |
| 30 | none | N | negative-control | stop | Floating point precision loss: 1/3 prints only 10 digits |
| 31 | none | N | negative-control | stop | 2^3 is wrong: it should be 1 (XOR), not 8 |
| 32 | rust | N | negative-control | stop | sign() returns 0 for positive numbers |
