


from flask import Flask, render_template, jsonify
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
     # Exécute un run et sauvegarde en base
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

if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000, debug=True)

@app.get("/")
def consignes():
     return render_template('consignes.html')

@app.route("/catfacts_test")
def catfacts_test():
     result = run_catfacts_test()
     return render_template_string("""
          <h2>Test Cat Facts</h2>
          <ul>
               <li>Status code: {{ result.get('status_code') }}</li>
               <li>Temps de réponse: {{ result.get('response_time') }} s</li>
               <li>Champ 'fact' valide: {{ result.get('fact_ok') }}</li>
               <li>Champ 'length' valide: {{ result.get('length_ok') }}</li>
               <li>Longueur cohérente: {{ result.get('length_match') }}</li>
               <li>Succès global: <b>{{ result.get('success') }}</b></li>
          </ul>
          <pre>{{ result.get('fact') }}</pre>
          {% if result.get('error') %}<p style='color:red;'>Erreur: {{ result.get('error') }}</p>{% endif %}
          <a href="/catfacts_results">Voir le tableau de résultats</a> | <a href="/">Retour</a>
     """, result=result)

@app.route("/catfacts_results")
def catfacts_results_table():
     return render_template_string("""
          <h2>Tableau des résultats Cat Facts (QoS)</h2>
          <table border="1" cellpadding="5">
               <tr>
                    <th>Date/Heure</th>
                    <th>Status</th>
                    <th>Temps (s)</th>
                    <th>Fact OK</th>
                    <th>Length OK</th>
                    <th>Longueur cohérente</th>
                    <th>Succès</th>
                    <th>Erreur</th>
                    <th>Fact</th>
               </tr>
               {% for r in results %}
               <tr>
                    <td>{{ r.timestamp }}</td>
                    <td>{{ r.status_code }}</td>
                    <td>{{ r.response_time }}</td>
                    <td>{{ r.fact_ok }}</td>
                    <td>{{ r.length_ok }}</td>
                    <td>{{ r.length_match }}</td>
                    <td style="color:{{ 'green' if r.success else 'red' }}; font-weight:bold;">{{ r.success }}</td>
                    <td>{{ r.get('error', '') }}</td>
                    <td>{{ r.fact }}</td>
               </tr>
               {% endfor %}
          </table>
          <a href="/">Retour</a>
     """, results=catfacts_results)

# Planification du test toutes les 5 minutes
def start_scheduler():
     scheduler = BackgroundScheduler()
     scheduler.add_job(run_catfacts_test, 'interval', minutes=5)
     scheduler.start()

if __name__ == "__main__":
     start_scheduler()
     app.run(host="0.0.0.0", port=5000, debug=True)
