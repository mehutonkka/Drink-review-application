from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash


def user_check(username):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone() 
    return user


def login(username, password):
    user = user_check(username)
    if not user:
        return 1
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            return 0
        
        

def signup(username, password, password1):
    user = user_check(username)
    if not user:
        if password == password1:
            hash_value = generate_password_hash(password)
            sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(sql, {"username":username, "password":hash_value})
            db.session.commit()
            return 0
        else:
            return 1
    


def list_profiles():
    result = db.session.execute(text("SELECT username FROM users"))
    return result.fetchall()


def search_profiles(search):
    result = db.session.execute(text("SELECT username FROM users WHERE lower(username) LIKE :search"), {"search":"%"+search+"%"})
    return result.fetchall()

   
def top5_users():
    sql = text("SELECT u.username, COUNT(r.user_id) FROM users u INNER JOIN reviews r ON u.id=r.user_id GROUP BY u.id ORDER BY COUNT(r.user_id) DESC LIMIT 5")
    result = db.session.execute(sql)
    return result.fetchall()