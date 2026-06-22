# TP2 — Injections et validation des entrées (Séance 2)

**Durée :** 1h40 | **Poids :** 20 % | **Travail :** individuel ou binôme

## Objectif

Exploiter puis corriger trois classes d'injections courantes en Python.

## Mise en place

```bash
cd tp2-injections
python -m venv .venv && source .venv/bin/activate
pip install -r ../../requirements.txt
pytest tests/ -v   # échoue tant que le code n'est pas corrigé
```

## Lab 1 — Injection SQL (40 min)

Fichier : `labs/sql_search.py`

- **Exploitation :** trouver un payload `username` qui retourne tous les utilisateurs.
- **Correction :** requêtes paramétrées ou ORM (SQLAlchemy).
- **Tests :** `tests/test_sql_search.py` (3 tests)

## Lab 2 — Injection de commande OS (30 min)

Fichier : `labs/command_runner.py`

- **Exploitation :** injecter une commande via le paramètre `host`.
- **Correction :** liste d'arguments, `shell=False`, validation allowlist.
- **Tests :** `tests/test_command_runner.py` (3 tests)

## Lab 3 — Path traversal (30 min)

Fichier : `labs/file_storage.py`

- **Exploitation :** lire un fichier hors du répertoire autorisé via `../`.
- **Correction :** `pathlib.resolve()`, vérification du préfixe, allowlist d'extensions.
- **Tests :** `tests/test_file_storage.py` (3 tests)

## Livrable

- Code corrigé dans `labs/`
- 9 tests pytest passants
- Brève note (`remediation.md`) : 1 paragraphe par vulnérabilité expliquant le correctif

## Rappel

> Ne jamais faire confiance aux entrées utilisateur. Préférer les **allowlists** aux blocklists.
