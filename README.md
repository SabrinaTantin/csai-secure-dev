# Développement sécurisé avec Python

## Prérequis

- Python 3.10+
- git, terminal, environnement virtuel

## Installation

Depuis la racine de ce repo :

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Travaux pratiques prévus

| TP | Dossier | Séance |
|----|---------|--------|
| TP1 | [tp1-audit](tp1-audit/) | S1 — Audit |
| TP2 | [tp2-injections](tp2-injections/) | S2 — Injections |
| TP3 | [tp3-auth](tp3-auth/) | S3 — Auth |
| TP4 | [tp4-web-api](tp4-web-api/) | S4 — API web |
| TP5 | [tp5-sast](tp5-sast/) | S5 — SAST |
| TP6 | [tp6-challenge](tp6-challenge/) | S6 — Challenge |

Chaque dossier contient un `README.md` avec l'énoncé et les livrables attendus.

## Validation de vos correctifs

```bash
# Depuis la racine du cours
make test
```

Les tests pytest définissent les critères de réussite. Ils **échouent volontairement** sur le code de départ.

## Aide-mémoire

[docs/secure-python-checklist.md](docs/secure-python-checklist.md) — sera disponible en fin de cours.
