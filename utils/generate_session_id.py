import secrets

def generate_session_for_user():
    session_id=secrets.token_hex(nbytes=16)
    return session_id
