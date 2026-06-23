# TP3 — Corrigé instructeur

## Failles du code de départ

| Faille | Risque |
|--------|--------|
| MD5 pour mots de passe | Crackage rapide (rainbow tables) |
| Secret hardcodé | Fuite via git, `/profile` |
| Cookie non HttpOnly | Vol de session via XSS |
| Token prévisible | `username:secret:timestamp` forgeable |
| Pas de rate limiting | Brute force sur `/login` |

## Points clés à expliquer en classe

1. **bcrypt** intègre salt + coût adaptatif — ne jamais implémenter son propre hash
2. **SESSION_SECRET** via `os.environ` — `.env` en dev seulement, jamais commité
3. **HttpOnly** empêche `document.cookie` ; **SameSite=Lax** limite CSRF
4. **Rate limiting** par IP : fenêtre glissante simple suffit pour le lab

## Validation

```bash
make test-solutions
# ou copier app/main.py vers student/tp3-auth/app/
```

## Erreurs fréquentes

- Remplacer MD5 par SHA-256 (toujours trop rapide pour passwords)
- Mettre le secret dans `.env` mais le laisser aussi en dur dans le code
- Oublier `httponly=True` dans `set_cookie`
