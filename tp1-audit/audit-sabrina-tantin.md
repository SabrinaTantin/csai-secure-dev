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


   ## 3. Top 3 des correctifs prioritaires
   
### 1. Supprimer la désérialisation `pickle`

La priorité numéro 1 concerne la fonction qui utilise `pickle.loads()` sur une donnée fournie par l’utilisateur. Cette vulnérabilité est critique car elle peut permettre à un attaquant d’exécuter du code côté serveur. Elle correspond à l’OWASP A08 — Software or Data Integrity Failures.

Le correctif prioritaire consiste à supprimer l’utilisation de `pickle` pour les données utilisateur. Il faut utiliser un format plus sûr, comme JSON, et valider strictement les champs attendus avant tout traitement.

### 2. Corriger l’injection SQL

La deuxième priorité concerne la route `/users/search`. Cette route utilise une entrée utilisateur dans une requête SQL. Si cette entrée n’est pas correctement contrôlée, un attaquant peut tenter de lire ou d’extraire des données de la base. Cette vulnérabilité correspond à l’OWASP A03 — Injection.

Le correctif consiste à utiliser des requêtes SQL paramétrées. Cela permet de séparer clairement la requête SQL des données saisies par l’utilisateur.

### 3. Sécuriser la configuration, les secrets et les fichiers

La troisième priorité concerne l’exposition d’informations sensibles et la gestion des fichiers. La route `/admin/config` expose la clé secrète Flask, le chemin de la base de données et le mode debug actif. Les routes d’upload et de téléchargement peuvent aussi permettre une lecture ou une écriture de fichiers non autorisée. Ces vulnérabilités correspondent notamment à l’OWASP A05 — Security Misconfiguration et A01 — Broken Access Control.

Les correctifs consistent à supprimer ou protéger la route `/admin/config`, placer les secrets dans des variables d’environnement, désactiver le mode debug, contrôler les extensions de fichiers autorisées et interdire les chemins dangereux comme `../`.

### Conclusion
Les corrections prioritaires doivent se concentrer sur la suppression de `pickle`, la sécurisation des requêtes SQL et la protection des fichiers et secrets.
