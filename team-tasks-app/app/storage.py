"""Simple in-memory user storage for demo purposes."""
from typing import Dict, List, Optional
from datetime import datetime

users_db: List[Dict] = []
_next_id = 1


def add_user(data: Dict) -> Dict:
    """Add a user dict to storage and assign an auto-increment id."""
    global _next_id
    now = datetime.utcnow()
    user = {
        "id": _next_id,
        "name": data["name"],
        "email": data["email"],
        "is_active": data.get("is_active", True),
        "created_at": now,
        **({"password_hash": data["password_hash"]} if "password_hash" in data else {}),
    }
    users_db.append(user)
    _next_id += 1
    return user


def find_by_email(email: str) -> Optional[Dict]:
    for u in users_db:
        if u.get("email") == email:
            return u
    return None


def find_by_id(user_id: int) -> Optional[Dict]:
    for u in users_db:
        if u.get("id") == user_id:
            return u
    return None
