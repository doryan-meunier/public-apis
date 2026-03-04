import requests

def test_cat_fact():
    url = "https://catfact.ninja/fact"
    response = requests.get(url)
    assert response.status_code == 200, f"Status code: {response.status_code}"  # QoS: disponibilité
    data = response.json()
    assert "fact" in data and isinstance(data["fact"], str), "Champ 'fact' absent ou mauvais type"
    assert "length" in data and isinstance(data["length"], int), "Champ 'length' absent ou mauvais type"
    assert data["length"] == len(data["fact"]), "Longueur incohérente"
    # Ajout d'une métrique simple: temps de réponse
    assert response.elapsed.total_seconds() < 2, f"Réponse trop lente: {response.elapsed.total_seconds()}s"

if __name__ == "__main__":
    test_cat_fact()
    print("Test Cat Facts OK")
