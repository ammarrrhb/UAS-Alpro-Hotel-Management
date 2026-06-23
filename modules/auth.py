# Credentials (in production, store hashed passwords in DB)
ADMIN_CREDENTIALS = {
    "admin": "hotel123",
    "manager": "manager456",
    "resepsionis": "resep789",
}

ADMIN_NAMES = {
    "admin": "Administrator",
    "manager": "Manager Hotel",
    "resepsionis": "Resepsionis",
}


def login(username: str, password: str) -> tuple[bool, str]:
    """
    Returns (success, display_name or error_message)
    """
    username = username.strip().lower()
    if username in ADMIN_CREDENTIALS:
        if ADMIN_CREDENTIALS[username] == password:
            return True, ADMIN_NAMES[username]
        else:
            return False, "Password salah. Silakan coba lagi."
    return False, "Username tidak ditemukan."
