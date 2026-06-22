# TP1 — Corrigé instructeur

## Vulnérabilités attendues

| # | Vulnérabilité | OWASP | Localisation | Exploitation |
|---|---------------|-------|--------------|--------------|
| 1 | Injection SQL | A03 Injection | `search_users()` | `?username=' OR '1'='1` |
| 2 | Hash MD5 | A02 Cryptographic Failures | `hash_password()` | Rainbow tables |
| 3 | Secret hardcodé | A02 / A05 | `APP_SECRET`, `/admin/config` | Fuite clé API |
| 4 | Path traversal | A01 Broken Access Control | `download_file()` | `?name=../../../etc/passwd` |
| 5 | Désérialisation pickle | A08 Software Integrity | `load_session()` | Payload pickle → RCE |
| 6 | Log mots de passe | A09 Logging Failures | `register_user()` | Credentials en clair dans les logs |
| 7 | Misconfiguration | A05 | `debug=True`, `0.0.0.0` | Console Werkzeug exposée |

Les étudiants doivent identifier **≥ 5** failles ; 6–7 comptent en bonus.

## Priorisation type (Top 3)

1. **Pickle** — exécution de code à distance, impact maximal
2. **SQL injection** — exfiltration / modification de la base
3. **Secret exposé via `/admin/config`** — compromission globale

## Pistes de correction (extrait)

```python
# SQL — requête paramétrée
conn.execute("SELECT ... WHERE username = ?", (username,))

# Mots de passe — bcrypt
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secrets — variable d'environnement
APP_SECRET = os.environ["APP_SECRET"]

# Fichiers — confinement
target = (UPLOAD_DIR / filename).resolve()
if not str(target).startswith(str(UPLOAD_DIR.resolve())):
    raise ValueError("Invalid path")

# Session — JSON signé ou JWT, jamais pickle
import json
session = json.loads(token.decode())

# Logs — ne jamais logger le mot de passe
logger.info("Register attempt username=%s", username)
```

## Erreurs fréquentes des étudiants

- Confondre « secret hardcodé » et « mot de passe faible » sans lier à OWASP
- Oublier la désérialisation pickle (moins visible que SQLi)
- Prioriser le debug mode avant pickle (impact moindre en lab local)

## Barème rappel

Schéma 2 pts | Identification 4 pts | Scénarios 2 pts | Priorisation 2 pts
