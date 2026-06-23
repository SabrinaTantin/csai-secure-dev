# TP5 — Supply chain et analyse statique (Séance 5)

**Durée :** 1h35

## Objectif

Analyser un projet Python avec Bandit et pip-audit, corriger les findings et automatiser les contrôles.

## Mise en place

```bash
cd tp5-sast
pip install -r ../requirements.txt
bandit pip-audit
```

## Énoncé

Le module `sample_project/` contient du code avec des anti-patterns détectables par Bandit :

- `eval()` sur entrée utilisateur
- `pickle.loads()` sur données non fiables
- `assert` utilisé pour validation (supprimé avec `-O`)
- Mot de passe hardcodé
- Logging de données sensibles

### Travail demandé

1. Exécuter `bandit -r sample_project -f txt` et sauvegarder le rapport **avant** correction
2. Exécuter `pip-audit` à la racine du cours et noter les CVE éventuelles
3. Corriger tous les findings **High** et **Medium** de Bandit
4. Ajouter un script ou job CI (voir `.github/workflows/security.yml` à compléter)
5. Produire un rapport **après** correction

## Livrable

- `reports/bandit-before.txt` et `reports/bandit-after.txt`
- Code corrigé dans `sample_project/`
- Workflow CI ou Makefile fonctionnel (`make security-check` à la racine)

## Commandes

```bash
bandit -r sample_project -ll
pip-audit -r ../../requirements.txt
```
