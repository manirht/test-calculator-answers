import io
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
