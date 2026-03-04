
# API Choice

- Étudiant : Doryan Meunier
- API choisie : Cat Facts
- URL base : https://catfact.ninja
- Documentation officielle / README : https://catfact.ninja/
- Auth : None
- Endpoints testés :
  - GET /fact
- Hypothèses de contrat (champs attendus, types, codes) :
  - champ "fact" (str), champ "length" (int), code 200
- Limites / rate limiting connu :
  - non documentées, généralement tolérantes
- Risques (instabilité, downtime, CORS, etc.) :
  - dépendance à un service externe, instabilité possible
