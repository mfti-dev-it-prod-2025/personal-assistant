from pwdlib import PasswordHash



class AuthAuthenticate:
    password_hash = PasswordHash.recommended()

    def authenticate_user(self, username: str, password: str):
        user = get_user(fake_db, username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user


    def verify_password(self, plain_password: str, hashed_password:str) -> bool:
        return self.password_hash.verify(plain_password, hashed_password)


    def get_password_hash(self, password: str) -> str:
        return self.password_hash.hash(password)