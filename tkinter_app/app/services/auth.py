from app.services.database import fetch_one

def authenticate(username, password):
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    user = fetch_one(query, (username, password))
    if user:
        return user
    return None
