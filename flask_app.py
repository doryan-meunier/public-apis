



from flask import Flask, render_template, jsonify, render_template_string
from tester.client import APIClient
from tester.tests import test_suite
from storage import list_runs, save_run
from datetime import datetime

app = Flask(__name__)

@app.get("/")
def consignes():
    return render_template('consignes.html')

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
    return "Run effectué et sauvegardé.<br><a href='/dashboard'>Voir le dashboard</a>"

@app.route("/dashboard")
def dashboard():
    runs = list_runs()
    return render_template("dashboard.html", runs=runs)
