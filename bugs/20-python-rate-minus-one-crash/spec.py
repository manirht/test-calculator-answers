BUG = dict(
    id="20", slug="python-rate-minus-one-crash", title="pv(-1, 3, 100) kills the Python helper",
    lang="python", also=["rust"], tier="L3", category="finance", kind="fix",
    commit_message="refactor: relax the rate lower bound check",
    issue=r'''
```
$ calc eval "pv(-1, 3, 100)"
error[EXTERNAL]: python process exited
```

A rate of -100% is nonsense but I'd expect a normal domain error like the one I get for -2 (`rate must be greater than -1`).
Instead the whole Python helper process dies. Running it again works only because the engine silently starts a new helper.
`fv(-1, 3, 100)` and `npv(-1, 10, 20)` behave the same way.
''',
    answer=dict(
        culprit="python/calcstats/finance.py::_check_rate",
        mechanism="The guard is `rate < -1` instead of `rate <= -1`. At exactly -1, `(1 + rate)` is 0 and `(1 + rate) ** -n` raises `ZeroDivisionError`, which `handle_request` does not catch (it only handles `CalcError`), so the helper process crashes. The Rust side reports it as EXTERNAL.",
        fix="`if rate <= -1:`. Optionally also catch `ZeroDivisionError` in `handle_request` and reply with a DOMAIN error.",
        grading="The symptom is on the Rust side but the cause is in Python. A thorough fix also hardens `handle_request` so that no function can take the process down; accept either, prefer both.",
        notes="The visible rate-floor test uses -2, which is rejected under either comparison.",
    ),
    expected={"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "root cause in Python"},
    edits=[("python/calcstats/finance.py", "    if rate <= -1:", "    if rate < -1:")],
    hidden={"python/tests/test_hidden_20.py": r'''import io
import json
import unittest

from calcstats import protocol


class RateMinusOne(unittest.TestCase):
    def test_pv_reports_a_domain_error(self):
        reply = protocol.handle_request({"id": 1, "fn": "pv", "args": ["-1", "3", "100"]})
        self.assertFalse(reply["ok"])
        self.assertEqual(reply["error"]["code"], "DOMAIN")

    def test_the_server_keeps_running(self):
        lines = [
            json.dumps({"id": 1, "fn": "npv", "args": ["-1", "10", "20"]}),
            json.dumps({"id": 2, "fn": "mean", "args": ["2", "4"]}),
        ]
        out = io.StringIO()
        protocol.serve(io.StringIO("\n".join(lines) + "\n"), out)
        replies = [json.loads(line) for line in out.getvalue().splitlines()]
        self.assertEqual([r["id"] for r in replies], [1, 2])
        self.assertEqual(replies[1]["value"], "3")


if __name__ == "__main__":
    unittest.main()
'''},
    run="cd python && python3 -m unittest discover -s tests -p test_hidden_20.py",
)
