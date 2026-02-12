import bcrypt

def hashed_user_password(user_password_bytes):
    # generate salt
    salt=bcrypt.gensalt(10)

    # hashing password
    hash_password=bcrypt.hashpw(user_password_bytes,salt).decode('utf-8')
    return hash_password