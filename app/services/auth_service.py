from app.database.database import SessionLocal
from app.database.user_model import UserDB
from app.security.jwt_handler import create_access_token


def register_user(user):
    db = SessionLocal()

    existing_user = db.query(UserDB).filter(
        UserDB.username == user.username
    ).first()

    if existing_user:
        db.close()
        raise ValueError("Username already exists")

    new_user = UserDB(
        username=user.username,
        password=user.password,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {"message": "User registered successfully"}


def login_user(username: str, password: str):
    db = SessionLocal()

    user = db.query(UserDB).filter(
        UserDB.username == username,
        UserDB.password == password
    ).first()

    db.close()

    if not user:
        raise ValueError("Invalid credentials")

    token = create_access_token({
        "sub": user.username,
        "user_id": user.id
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }