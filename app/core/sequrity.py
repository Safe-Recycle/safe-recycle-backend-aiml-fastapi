from pwdlib import PasswordHash
from sqlmodel import Session, select
from app.models.user_model import User

password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hashed(password):
    return password_hash.hash(password)

def get_user_by_email(session: Session, email: str) -> User | None:
    return session.exec(
        select(User).where(User.email == email)
    ).first()