



from flask import Flask, render_template, jsonify, render_template_string
from tester.client import APIClient
from tester.tests import test_suite
from storage import list_runs, save_run
from datetime import datetime

app = Flask(__name__)



@app.route("/run")
def run_tests():
    API_NAME = "Cat Facts"
    BASE_URL = "https://catfact.ninja"
    ENDPOINT = "/fact"
    client = APIClient(BASE_URL)
    resp = client.get(ENDPOINT)
    results = []
    for name, test in test_suite:
        try:
            passed = test(resp)
        except Exception:
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
    return render_template("run.html", run=run)

@app.route("/dashboard")

def dashboard():
    runs = list_runs()
    return render_template("dashboard.html", runs=runs)

# BONUS : Endpoint /health
@app.route("/health")
def health():
    runs = list_runs(1)
    if runs:
        last = runs[0]
        status = "OK" if last["summary"]["error_rate"] == 0 else "DEGRADED"
        return render_template("health.html",
            status=status,
            last_run=last["timestamp"],
            error_rate=last["summary"]["error_rate"],
            latency_ms_avg=last["summary"]["latency_ms_avg"])
    return render_template("health.html", status="NO DATA")

# BONUS : Export JSON de l'historique
@app.route("/export")
def export():
    runs = list_runs(50)
    return jsonify(runs)
