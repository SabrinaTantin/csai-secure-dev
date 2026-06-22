# TP2 — Remédiation des injections

## Injection SQL

La vulnérabilité venait de l’utilisation d’une entrée utilisateur dans une requête SQL. Le correctif consiste à utiliser une requête paramétrée avec un placeholder `?`. Ainsi, la valeur de `username` est traitée comme une donnée et non comme du code SQL. Cela empêche un payload comme `' OR '1'='1` de retourner tous les utilisateurs.

## Injection de commande OS

La vulnérabilité venait de l’exécution d’une commande système construite à partir du paramètre `host`. Le correctif consiste à refuser les métacaractères shell, à valider l’hôte avec une allowlist, puis à exécuter la commande sous forme de liste d’arguments avec `shell=False`. Ainsi, un payload comme `127.0.0.1; echo PWNED` n’est pas exécuté.

## Path traversal

La vulnérabilité venait de la lecture ou de l’écriture de fichiers à partir d’un chemin fourni par l’utilisateur. Le correctif consiste à résoudre le chemin avec `pathlib.resolve()`, vérifier que le chemin final reste dans le répertoire autorisé `STORAGE_ROOT`, et limiter les extensions autorisées. Cela empêche l’accès à des fichiers situés hors du dossier prévu via `../`.
