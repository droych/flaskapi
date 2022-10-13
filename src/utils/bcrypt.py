import bcrypt

def encrypt_password(password):
    pwhash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    hashed = pwhash.decode('utf8')
    return hashed


def compare_passwords(password, hashed_password):
    if bcrypt.checkpw(password, hashed_password):
        return True
    else:
        return False