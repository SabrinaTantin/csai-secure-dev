# TP3 — Authentification, sessions et secrets (Séance 3)

**Durée :** 1h35 | **Poids :** 20 %

## Objectif

Sécuriser un endpoint `/login` FastAPI en corrigeant le stockage des mots de passe, la gestion de session et les secrets.

## Mise en place

```bash
cd tp3-auth
cp .env.example .env
# Éditer .env avec SESSION_SECRET généré via: python -c "import secrets; print(secrets.token_hex(32))"
pip install -r ../../requirements.txt
uvicorn app.main:app --reload --port 5003
```

## Énoncé

Le fichier `app/main.py` contient volontairement :

1. Hash MD5 des mots de passe
2. Secret de session hardcodé
3. Cookie de session non HttpOnly / non Secure
4. Absence de rate limiting sur `/login`

### Travail demandé

1. Remplacer MD5 par **bcrypt** (via `passlib`)
2. Charger `SESSION_SECRET` depuis les variables d'environnement
3. Configurer le cookie : `httponly=True`, `secure=True` (dev : commenter secure si HTTP), `samesite="lax"`
4. Ajouter un rate limiting basique (ex. max 5 tentatives / minute / IP)
5. Fournir un `.env.example` sans valeur secrète réelle

## Tests

```bash
pytest tests/ -v
```

## Livrable

- `app/main.py` corrigé
- `.env.example`
- Captures ou logs montrant un login réussi et un rejet après rate limit
