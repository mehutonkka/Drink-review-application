from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash


def user_check(username):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
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
            sql = text(
                "INSERT INTO users (username, password, admin)\
                      VALUES (:username, :password, False)"
            )
            db.session.execute(sql, {"username": username, "password": hash_value})
            db.session.commit()
            return 0
        else:
            return 1


def list_profiles():
    result = db.session.execute(text("SELECT id, username FROM users"))
    return result.fetchall()


def search_profiles(search):
    result = db.session.execute(
        text("SELECT username FROM users WHERE lower(username) LIKE :search"),
        {"search": "%" + search + "%"},
    )
    return result.fetchall()


def top5_users():
    sql = text(
        "SELECT u.username, COUNT(r.user_id)\
              FROM users u INNER JOIN reviews r \
                ON u.id=r.user_id GROUP BY u.id \
                    ORDER BY COUNT(r.user_id) DESC LIMIT 5"
    )
    result = db.session.execute(sql)
    return result.fetchall()


def check_admin():
    result = db.session.execute(text("SELECT * FROM users WHERE admin='t'"))
    if result.fetchall():
        return True
    else:
        return False


def is_admin(username):
    result = db.session.execute(
        text("SELECT admin FROM users WHERE username=:username"), 
        {"username": username}
    )
    result = result.fetchone()[0]
    if result == True:
        return result


def create_admin(username):
    sql = text("UPDATE users SET admin = True WHERE username=:username")
    db.session.execute(sql, {"username": username})
    db.session.commit()


def delete_user(user_id):
    sql = text("DELETE FROM users WHERE id=:user_id")
    db.session.execute(sql, {"user_id": user_id})
    sql2 = text("DELETE FROM reviews WHERE user_id=:user_id")
    db.session.execute(sql2, {"user_id": user_id})
    db.session.commit()
