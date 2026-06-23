# TP4 — Sécurité des applications web Python (Séance 4)

**Durée :** 1h40

## Objectif

Durcir une API REST FastAPI : validation stricte, protection XSS, en-têtes de sécurité HTTP.

## Mise en place

```bash
cd tp4-web-api
pip install -r ../../requirements.txt
uvicorn app.main:app --reload --port 5004
```

## Énoncé

L'API `app/main.py` expose un mini-CRUD de notes. Elle contient :

1. XSS stocké via le champ `content` (renvoyé sans échappement)
2. Absence d'en-têtes de sécurité (CSP, X-Frame-Options, etc.)
3. Validation insuffisante des entrées (pas de limite de taille, caractères dangereux)
4. CORS permissif (`allow_origins=["*"]`)

### Travail demandé

1. Ajouter des modèles **Pydantic** stricts (`Field(max_length=...)`, validators)
2. Échapper ou sanitiser le contenu HTML avant stockage ou à l'affichage
3. Ajouter un middleware d'en-têtes de sécurité OWASP
4. Restreindre CORS à `http://localhost:3000` (ou origine de dev)
5. Tester une requête malveillante avec `curl` et documenter le rejet

Exemple de payload XSS :

```bash
curl -X POST http://127.0.0.1:5004/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"test","content":"<script>alert(1)</script>"}'
```

## Tests

```bash
pytest tests/ -v
```

## Livrable

- API corrigée
- Fichier `proof.md` : commande curl + réponse montrant mitigation XSS ou headers présents
