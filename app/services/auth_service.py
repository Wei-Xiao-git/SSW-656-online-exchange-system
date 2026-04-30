from app.database.database import fake_users_db


def register_user(user):
    for existing_user in fake_users_db:
        if existing_user.username == user.username:
            raise ValueError("Username already exists")

    fake_users_db.append(user)

    return {"message": "User registered successfully"}


def login_user(username: str, password: str):
    for user in fake_users_db:
        if user.username == username and user.password == password:
            return {"message": "Login successful"}

    raise ValueError("Invalid credentials")