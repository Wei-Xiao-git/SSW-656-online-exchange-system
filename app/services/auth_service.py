from app.database.database import SessionLocal
from app.database.user_model import UserDB


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

    if user:
        return {"message": "Login successful"}

    raise ValueError("Invalid credentials")