import ast
import json
import logging
import os
import hmac

logger = logging.getLogger(__name__)


def run_user_formula(formula: str) -> int:
    """
    Évalue uniquement des valeurs littérales sûres.
    Remplace eval() qui exécute du code arbitraire.
    """
    try:
        value = ast.literal_eval(formula)
    except (ValueError, SyntaxError) as exc:
        raise ValueError("Formule invalide") from exc

    if not isinstance(value, int):
        raise ValueError("La formule doit retourner un entier")

    return value


def restore_session(blob: bytes) -> dict:
    """
    Remplace pickle.loads() par json.loads().
    pickle est dangereux sur des données non fiables.
    """
    try:
        data = json.loads(blob.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("Session invalide") from exc

    if not isinstance(data, dict):
        raise ValueError("La session doit être un dictionnaire")

    return data


def check_admin_password(password: str) -> bool:
    """
    Remplace assert par une validation explicite.
    Le mot de passe attendu vient d'une variable d'environnement.
    """
    expected_password = os.environ.get("ADMIN_PASSWORD")

    if not expected_password:
        logger.error("ADMIN_PASSWORD non configuré")
        return False

    return hmac.compare_digest(password, expected_password)


def authenticate(username: str, password: str) -> bool:
    """
    Ne journalise plus le mot de passe.
    """
    logger.warning("Auth attempt user=%s", username)

    if username != "admin":
        return False

    return check_admin_password(password)
