import bcrypt

def hash_password(plain_password: str) -> bytes:
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

if __name__ == "__main__":
    original_password = "mysecretpassword"
    hashed = hash_password(original_password)
    print("해싱된 비밀번호:", hashed)

    if verify_password(original_password, hashed):
        print("비밀번호 일치")
    else:
        print("비밀번호 불일치")
