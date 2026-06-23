# TP4 — Preuve de mitigation XSS et headers de sécurité

## 1. Test du payload XSS

Commande utilisée :

curl -i -X POST http://127.0.0.1:5004/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"test","content":"<script>alert(1)</script>"}'

Objectif :
Vérifier que le payload XSS <script>alert(1)</script> est neutralisé par l'application.

## 2. Vérification de la restitution HTML

Commande utilisée :

curl -i http://127.0.0.1:5004/notes/1

Résultat attendu :
Le HTML retourné ne contient pas de balise <script> exécutable.
Le contenu est échappé avec html.escape.

## 3. Vérification des en-têtes de sécurité

Commande utilisée :

curl -I http://127.0.0.1:5004/notes

Headers attendus :
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'; script-src 'self'
Strict-Transport-Security: max-age=31536000; includeSubDomains

## 4. Corrections réalisées

- Modèle Pydantic strict avec Field(min_length=..., max_length=...).
- Validation des contenus dangereux avec field_validator.
- Mitigation XSS avec html.escape.
- Middleware d'en-têtes de sécurité HTTP.
- CORS restrictif limité à http://localhost:3000.

## Conclusion

L'API REST FastAPI a été durcie contre les risques XSS, les entrées insuffisamment validées, les en-têtes de sécurité absents et le CORS trop permissif.
