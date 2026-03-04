import json
from datetime import datetime
from tester.client import APIClient
from tester.tests import test_suite
from storage import save_run

API_NAME = "Cat Facts"
BASE_URL = "https://catfact.ninja"
ENDPOINT = "/fact"

client = APIClient(BASE_URL)
resp = client.get(ENDPOINT)

results = []
for name, test in test_suite:
    try:
        passed = test(resp)
    except Exception as e:
        passed = False
    results.append({"name": name, "status": "PASS" if passed else "FAIL"})

summary = {
    "passed": sum(1 for r in results if r["status"] == "PASS"),
    "failed": sum(1 for r in results if r["status"] == "FAIL"),
    "error_rate": sum(1 for r in results if r["status"] == "FAIL") / len(results),
    "latency_ms_avg": resp["latency_ms"] if resp["latency_ms"] is not None else None,
    "latency_ms_p95": resp["latency_ms"] if resp["latency_ms"] is not None else None
}

run = {
    "api": API_NAME,
    "timestamp": datetime.now().isoformat(),
    "summary": summary,
    "tests": results
}

save_run(run)

if __name__ == "__main__":
    print(json.dumps(run, indent=2, ensure_ascii=False))
