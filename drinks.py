from db import db
from sqlalchemy.sql import text

def list_drinks():
    result = db.session.execute(text("SELECT * FROM drinks ORDER BY drinks.name"))
    drinks = result.fetchall()
    return drinks


def category_list():
    result = db.session.execute(text("SELECT * FROM categories"))
    return result.fetchall()

def store_list():
    result = db.session.execute(text("SELECT * FROM stores"))
    return result.fetchall()

def drink_check(drink_name):
    sql = text("SELECT id FROM drinks WHERE name=:name")
    result = db.session.execute(sql, {"name":drink_name})
    return result.fetchone()

def create_drink(name, percentage, category_id, store_ids, price):
    store_ids2 = []
    check = drink_check(name)
    if not check:
        for store in store_ids:
            result = db.session.execute(text("SELECT id from stores WHERE name=:name"), {"name":store})
            store_ids2.append(result.fetchone()[0])
        categ_id = db.session.execute(text("SELECT id from categories WHERE category=:category"), {"category":category_id})
        categ_id2 = categ_id.fetchone()[0]
        sql = (text("INSERT INTO drinks (name, percentage, category_id, store_ids, price) VALUES (:name, :percentage, :category_id, :store_ids, :price)"))
        db.session.execute(sql, {"name":name, "percentage":percentage, "category_id":categ_id2, "store_ids":store_ids2, "price":price})
        db.session.commit()
        return 0
    else:
        return 1
    

def list_search(search_input):
    result = db.session.execute(text("SELECT * FROM drinks WHERE lower(name) LIKE :search"), {"search":"%"+search_input+"%"})
    drinks = result.fetchall()
    return drinks

def list_search_category(search_input, category_id):
    if search_input != None:
        result = db.session.execute(text("SELECT * FROM drinks WHERE lower(name) LIKE :search AND category_id=:category_id"), {"search":"%"+search_input+"%", "category_id":category_id})
    else:
        result = db.session.execute(text("SELECT * FROM drinks WHERE category_id=:category_id"), {"category_id":category_id})
    drinks = result.fetchall()
    return drinks

def drink_name(drink_id):
    result = db.session.execute(text("SELECT id, name, percentage, price FROM drinks WHERE id=:drink_id"), {"drink_id":drink_id})
    return result.fetchone()

def drink_stores(drink_id):
    result = db.session.execute(text("SELECT store_ids FROM drinks WHERE id=:drink_id"), {"drink_id":drink_id})
    stores = result.fetchone()
    stores_written = []
    for store in stores[0]:
        if store!="{" and store!="}" and store!=",":
            result2 = db.session.execute(text("SELECT name FROM stores WHERE id=:store"), {"store":store})
            name = result2.fetchone()
            stores_written.append(name)
    return stores_written

def drink_category(drink_id):
    result = db.session.execute(text("SELECT categories.category FROM categories, drinks WHERE categories.id=CAST(drinks.category_id AS INTEGER) AND drinks.id=:drink_id "), {"drink_id":drink_id})
    return result.fetchone()[0]


def create_new_review(drink_id, user_name, review, score):
    score = int(score)
    user_id = int(db.session.execute(text("SELECT id FROM users where username=:name"), {"name":user_name}).fetchone()[0])
    check = db.session.execute(text("SELECT id FROM reviews WHERE drink_id=:drink_id AND user_id=:user_id"), {"drink_id":drink_id, "user_id":user_id})
    check = check.fetchone()
    if not check:
        sql = text("INSERT INTO reviews (drink_id, user_id, review, score) VALUES (:drink_id, :user_id, :review, :score)")
        db.session.execute(sql, {"drink_id":drink_id, "user_id":user_id, "review":review, "score":score})
    else:
        check = check[0]
        sql = text("UPDATE reviews SET drink_id=:drink_id, user_id=:user_id, review=:review, score=:score WHERE id=:check")
        db.session.execute(sql, {"drink_id":drink_id, "user_id":user_id, "review":review, "score":score, "check":check})
    db.session.commit()


    
def list_reviews(drink_id):
    result = db.session.execute(text("SELECT reviews.*, users.username FROM reviews, users WHERE reviews.drink_id=:drink_id and reviews.user_id=users.id ORDER BY reviews.drink_id DESC"), {"drink_id":drink_id})
    return result.fetchall()

def list_user_reviews(user_id):
    result = db.session.execute(text("SELECT reviews.*, drinks.name FROM reviews, drinks WHERE reviews.drink_id=drinks.id AND user_id=:user_id"), {"user_id":user_id})
    return result.fetchall()

def top_10_drinks():
    sql = text("SELECT d.name, d.id, AVG(r.score)::numeric(10,1) from reviews r INNER JOIN drinks d ON r.drink_id=d.id GROUP BY d.name, d.id ORDER BY avg(r.score) DESC LIMIT 10")
    result = db.session.execute(sql)
    return result.fetchall()

def recent_reviews():
    result = db.session.execute(text("SELECT reviews.*, users.username, drinks.name FROM reviews, users, drinks WHERE reviews.user_id=users.id AND reviews.drink_id=drinks.id ORDER BY id DESC LIMIT 3"))
    return result.fetchall()

def new_drinks():
    result = db.session.execute(text("SELECT d.*, c.category FROM drinks d, categories c WHERE CAST(d.category_id AS INTEGER)=c.id ORDER BY d.id DESC"))
    return result.fetchmany(3)

def delete(drink_id):
    sql = text("DELETE FROM drinks WHERE id=:drink_id")
    db.session.execute(sql, {"drink_id":drink_id})
    db.session.commit()

def delete_review(review_id):
    sql = text("DELETE FROM reviews WHERE id=:review_id")
    db.session.execute(sql, {"review_id":review_id})
    db.session.commit()