# TP1 — Audit de sécurité d’une application Flask vulnérable

## 1. Schéma de flux applicatif

```text
Utilisateur / Attaquant
        |
        v
Application Flask
        |
        +--> /users/search
        |       Entrée : username
        |       Traitement : requête SQL
        |       Données : base SQLite users.db
        |
        +--> /users/register
        |       Entrées : username, password
        |       Traitement : hash MD5 + logs
        |       Données : base SQLite users.db
        |
        +--> /files/upload
        |       Entrée : fichier + nom de fichier
        |       Données : dossier uploads
        |
        +--> /files/download
        |       Entrée : nom de fichier
        |       Sortie : fichier téléchargé
        |
        +--> /session/load
        |       Entrée : token de session
        |       Traitement : désérialisation pickle
        |
        +--> /admin/config
                Sortie : informations de configuration sensibles
```

## 2. Vulnérabilités identifiées

| Vulnérabilité                      | OWASP                                       | Fonction concernée    | Scénario d’exploitation                                                                                            | Gravité  |
| ---------------------------------- | ------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------ | -------- |
| Injection SQL                      | A03: Injection                              | `search_users()`      | Un attaquant peut modifier la requête SQL via le paramètre `username` afin d’accéder à des données non autorisées. | Critique |
| Mot de passe administrateur faible | A07: Authentication Failures                | `init_db()`           | Le compte administrateur utilise un mot de passe faible et facilement devinable.                                   | Haute    |
| Hash MD5 des mots de passe         | A02: Cryptographic Failures                 | `hash_password()`     | MD5 est obsolète et vulnérable aux attaques par dictionnaire ou rainbow tables.                                    | Haute    |
| Journalisation des mots de passe   | A09: Security Logging and Alerting Failures | `register_user()`     | Les mots de passe peuvent apparaître dans les logs applicatifs.                                                    | Haute    |
| Upload de fichier non contrôlé     | A01: Broken Access Control                  | `upload_file()`       | Un attaquant peut envoyer un fichier avec un nom malveillant et écrire hors du dossier prévu.                      | Haute    |
| Téléchargement non contrôlé        | A01: Broken Access Control                  | `download_file()`     | Un attaquant peut tenter de lire des fichiers sensibles avec un chemin de type `../`.                              | Haute    |
| Désérialisation non sécurisée      | A08: Software or Data Integrity Failures    | `load_session()`      | L’utilisation de `pickle.loads()` sur une entrée utilisateur peut permettre l’exécution de code arbitraire.        | Critique |
| Exposition de secrets              | A05: Security Misconfiguration              | `admin_config()`      | La route expose la clé secrète Flask et le chemin de la base de données.                                           | Haute    |
| Mode debug activé                  | A05: Security Misconfiguration              | `app.run(debug=True)` | Le mode debug peut exposer des informations techniques sensibles.                                                  | Haute    |

## 3. Top 3 des correctifs prioritaires

### 1. Supprimer la désérialisation `pickle`

La fonction `pickle.loads()` ne doit jamais être utilisée sur une donnée fournie par l’utilisateur.
Il faut la remplacer par un format plus sûr comme JSON, avec une validation stricte des champs attendus.

### 2. Corriger l’injection SQL

Les requêtes SQL doivent être paramétrées afin d’éviter l’injection SQL.

Exemple de correction :

```python
conn.execute(
    "SELECT id, username FROM users WHERE username = ?",
    (username,)
)
```

### 3. Sécuriser la gestion des fichiers et de la configuration

Il faut valider les noms de fichiers, interdire les chemins relatifs dangereux comme `../`, limiter les extensions autorisées, désactiver le mode debug et ne jamais exposer les secrets applicatifs via une route comme `/admin/config`.

## Conclusion

L’application contient plusieurs vulnérabilités critiques permettant potentiellement l’accès non autorisé aux données, la lecture ou l’écriture de fichiers, l’exposition de secrets et l’exécution de code côté serveur.

Les corrections prioritaires doivent se concentrer sur la suppression de `pickle`, la sécurisation des requêtes SQL et la protection des fichiers et secrets.
