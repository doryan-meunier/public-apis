import requests
import time

class APIClient:
    def __init__(self, base_url, timeout=3, max_retries=1):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        for attempt in range(self.max_retries + 1):
            try:
                start = time.time()
                response = requests.get(url, params=params, timeout=self.timeout)
                latency = int((time.time() - start) * 1000)
                if response.status_code == 429 and attempt < self.max_retries:
                    time.sleep(2)  # simple backoff
                    continue
                return {
                    "status_code": response.status_code,
                    "latency_ms": latency,
                    "json": response.json() if response.headers.get('Content-Type', '').startswith('application/json') else None,
                    "error": None
                }
            except requests.exceptions.Timeout:
                if attempt < self.max_retries:
                    continue
                return {"status_code": None, "latency_ms": None, "json": None, "error": "timeout"}
            except Exception as e:
                return {"status_code": None, "latency_ms": None, "json": None, "error": str(e)}
        return {"status_code": None, "latency_ms": None, "json": None, "error": "max retries exceeded"}
