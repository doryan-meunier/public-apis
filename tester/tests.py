def test_status_code(resp):
    return resp["status_code"] == 200

def test_content_type(resp):
    return resp["json"] is not None

def test_fact_field(resp):
    return resp["json"] and "fact" in resp["json"] and isinstance(resp["json"]["fact"], str)

def test_length_field(resp):
    return resp["json"] and "length" in resp["json"] and isinstance(resp["json"]["length"], int)

def test_length_match(resp):
    return resp["json"] and resp["json"]["length"] == len(resp["json"]["fact"])

def test_latency(resp):
    return resp["latency_ms"] is not None and resp["latency_ms"] < 2000

def test_no_error(resp):
    return resp["error"] is None

test_suite = [
    ("Status code 200", test_status_code),
    ("Content-Type JSON", test_content_type),
    ("Champ 'fact' présent", test_fact_field),
    ("Champ 'length' présent", test_length_field),
    ("Longueur cohérente", test_length_match),
    ("Latence < 2s", test_latency),
    ("Pas d'erreur", test_no_error)
]
