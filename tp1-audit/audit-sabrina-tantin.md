Ce livrable présente l’audit de sécurité du TP1. L’analyse porte sur les flux applicatifs, les vulnérabilités identifiées, leur correspondance avec l’OWASP Top 10 et les correctifs prioritaires à mettre en oeuvre.

# TP1 — Audit de sécurité d’une application Flask vulnérable

## 1. Schéma de flux applicatif.

text
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


Script / fonction| 	Élément observé	Vulnérabilité associée
APP_SECRET = "super-secret-key-do-not-share"	| Clé secrète écrite en dur dans le code	| Exposition de secret — OWASP A05
init_db()	| Création d’un compte admin avec le mot de passe admin123| 	Authentification faible — OWASP A07
hash_password()	| Utilisation de hashlib.md5() pour hacher les mots de passe| 	Mauvais mécanisme cryptographique — OWASP A02
search_users()	| Requête SQL construite avec une entrée utilisateur username	| Injection SQL — OWASP A03
register_user()	| Journalisation du mot de passe dans les logs	| Fuite d’information dans les logs — OWASP A09
upload_file()	| Écriture d’un fichier avec un nom fourni par l’utilisateur	| Upload non contrôlé / path traversal — OWASP A01
download_file()	| Lecture d’un fichier à partir d’un paramètre utilisateur name	| Téléchargement non contrôlé — OWASP A01
load_session()	| Utilisation de pickle.loads() sur des données reçues en POST| 	Désérialisation dangereuse — OWASP A08
admin_config()| 	Exposition du chemin de la base, du mode debug et de la clé secrète	| Mauvaise configuration — OWASP A05
app.run(debug=True)	| Lancement de Flask en mode debug| 	Mauvaise configuration — OWASP A05



## 5. Corrections proposées pour 5 vulnérabilités

| Vulnérabilité corrigée | Correction à appliquer | Objectif de sécurité |
|---|---|---|
| Injection SQL dans `/users/search` | Remplacer la requête SQL construite avec une entrée utilisateur par une requête paramétrée. | Empêcher l’injection SQL et protéger la base de données. |
| Désérialisation dangereuse dans `/session/load` | Supprimer `pickle.loads()` et utiliser un format sûr comme JSON avec validation stricte des champs. | Éviter l’exécution de code arbitraire côté serveur. |
| Hash MD5 des mots de passe | Remplacer `hashlib.md5()` par un algorithme adapté au stockage des mots de passe, par exemple `bcrypt` ou `werkzeug.security.generate_password_hash`. | Renforcer la protection des mots de passe. |
| Exposition de secrets via `/admin/config` | Supprimer la route ou la protéger par authentification, et déplacer la clé secrète dans une variable d’environnement. | Éviter la fuite de secrets applicatifs. |
| Upload/téléchargement de fichiers non contrôlés | Utiliser `secure_filename()`, vérifier les extensions autorisées et empêcher les chemins contenant `../`. | Empêcher la lecture ou l’écriture de fichiers non autorisés. |

### Conclusion
Les corrections prioritaires doivent se concentrer sur la suppression de `pickle`, la sécurisation des requêtes SQL et la protection des fichiers et secrets.
