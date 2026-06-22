# TP1 — Audit d'une mini-application vulnérable (Séance 1)

**Durée :** 1h30 | **Travail :** binôme

## Objectif

Cartographier les flux de données d'une application Python, identifier les vulnérabilités introduites volontairement et proposer des correctifs priorisés.

## Mise en place

Depuis la **racine de ce repo** :

```bash
make install
make run-tp1
```

Si erreur Flask ou « environnement incohérent » :

```bash
make reinstall
make run-tp1
```

**Prérequis :** Python **3.10+**.

L'application expose une API Flask sur `http://127.0.0.1:5001`.

### Erreur `ModuleNotFoundError: No module named 'flask'`

Le venv a été créé avec une version de Python différente de celle utilisée par `pip`.

```bash
cd courses/secure-python
make reinstall
make run-tp1
```

## Énoncé

1. **Cartographie (20 min)** — Dessinez un schéma des flux : entrées utilisateur → traitements → stockage / sorties.
2. **Audit (45 min)** — Parcourez le code de `app/vulnerable_app.py` et listez **au minimum 5 vulnérabilités** avec :
   - Catégorie OWASP
   - Fichier / fonction concernée
   - Scénario d'exploitation (comment un attaquant en profiterait)
   - Gravité (Critique / Haute / Moyenne / Basse)
3. **Priorisation (25 min)** — Classez vos correctifs par ordre de priorité (matrice impact × effort).

## Indice (ne pas ouvrir avant 30 min de travail)

<details>
<summary>Zones à inspecter</summary>

- Gestion des utilisateurs et mots de passe
- Requêtes base de données
- Upload de fichiers
- Configuration et secrets
- Journalisation

</details>

## Livrable

Fichier `audit-<nom1>-<nom2>.md` (1 page max) contenant :

1. Schéma de flux (image ou ASCII)
2. Tableau des vulnérabilités (≥ 5 lignes)
3. Top 3 des correctifs à implémenter en priorité

## Critères de réussite

- Au moins 5 vulnérabilités identifiées correctement
- Lien explicite avec OWASP Top 10
- Priorisation argumentée (pas seulement une liste)
