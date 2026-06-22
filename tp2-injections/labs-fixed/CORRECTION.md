# TP2 — Corrigé instructeur

## Lab 1 — SQL (`sql_search.py`)

**Problème :** concaténation de la variable `username` dans la requête SQL.

**Correction :** placeholder `?` et tuple de paramètres. Le driver SQLite échappe les valeurs ; la structure SQL reste fixe.

```python
query = "SELECT id, username FROM users WHERE username = ?"
rows = conn.execute(query, (username,)).fetchall()
```

**Pourquoi ça marche :** l'injection `' OR '1'='1` devient une **valeur littérale** recherchée, pas du code SQL exécutable.

---

## Lab 2 — Command injection (`command_runner.py`)

**Problème :** `shell=True` + f-string → le shell interprète `;`, `$()`, etc.

**Correction :**

1. `shell=False` avec liste d'arguments `["ping", "-c", "1", host]`
2. Allowlist sur le hostname : regex `^[\w.-]+$` ou validation IP via `ipaddress`

```python
if not HOST_PATTERN.match(host):
    raise ValueError("Invalid host")
subprocess.run(["ping", "-c", "1", host], shell=False, ...)
```

**Pourquoi :** sans shell, `127.0.0.1; echo PWNED` est passé comme **un seul argument** à `ping`, pas comme deux commandes.

---

## Lab 3 — Path traversal (`file_storage.py`)

**Problème :** `STORAGE_ROOT / "../secret.txt"` sort du répertoire autorisé.

**Correction :**

```python
def _safe_path(filename: str) -> Path:
    target = (STORAGE_ROOT / filename).resolve()
    root = STORAGE_ROOT.resolve()
    if not str(target).startswith(str(root)):
        raise ValueError("Path traversal detected")
    return target
```

**Pourquoi :** `resolve()` normalise `..` ; le test de préfixe garantit que le fichier final reste sous `STORAGE_ROOT`.

---

## Validation

```bash
make test-student   # échoue sur code vulnérable
cp instructor/solutions/tp2-injections/labs/*.py student/tp2-injections/labs/
make test-student   # 9/9 passants
```

## Erreurs fréquentes

- Échapper manuellement les quotes SQL (`replace("'", "''")`) au lieu de paramétrer
- Blocklist de caractères (`;`, `|`) au lieu de supprimer `shell=True`
- Oublier `.resolve()` avant le test de préfixe
