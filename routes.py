from app import app
import users
import drinks
from flask import redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
import secrets


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


# Functionality to login to the website and to be redirected to the home page
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if len(username) > 20:
        return render_template("index.html", login_message="Username is too long!")
    if len(password) > 30:
        return render_template("index.html", login_message="Password is too long!")

    result = users.login(username, password)
    if result == 1:
        return render_template("index.html", login_message="Incorrect username!")
    elif result == 0:
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/home_page")
    else:
        return render_template(
            "index.html", login_message="Incorrect username/password!"
        )


# Functionality to signup/create a new user and be redirected to the home page
@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    password1 = request.form["password1"]
    if len(username) > 20:
        return render_template("index.html", signup_message="Username is too long!")
    if len(password) > 30:
        return render_template("index.html", signup_message="Password is too long!")
    result = users.signup(username, password, password1)
    if result == 0:
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/home_page")
    elif result == 1:
        return render_template(
            "index.html", signup_message="The two passwords do not match!"
        )
    else:
        return render_template(
            "index.html", signup_message="That username is already in use!"
        )


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/home_page", methods=["GET", "POST"])
def home_page():
    top10 = drinks.top_10_drinks()
    top5 = users.top5_users()
    return render_template("home_page.html", top10=top10, top5=top5)


@app.route("/recent")
def recent():
    recent = drinks.recent_reviews()
    new = drinks.new_drinks()
    return render_template("recent_activity.html", recent=recent, new=new)


@app.route("/drinks")
def drinks_page():
    categories = drinks.category_list()
    result = drinks.list_drinks()
    return render_template("drinks.html", result=result, categories=categories)


@app.route("/drinks_s", methods=["GET"])
def drinks_search_page():
    categories = drinks.category_list()
    s_filter = request.args["s_filter"]
    category_id = request.args["category_id"]
    if s_filter:
        if category_id != "0":
            result = drinks.list_search_category(s_filter, category_id)
        else:
            result = drinks.list_search(s_filter)
    else:
        if category_id != "0":
            result = drinks.list_search_category(None, category_id)
        else:
            result = drinks.list_drinks()
    return render_template("drinks.html", result=result, categories=categories)


@app.route("/drink/<int:drink_id>")
def drink_page(drink_id):
    result = drinks.drink_name(drink_id)
    stores = drinks.drink_stores(drink_id)
    category = drinks.drink_category(drink_id)
    reviews = drinks.list_reviews(drink_id)
    score = drinks.drink_score(drink_id)
    try:
        admin = users.is_admin(session["username"])
    except:
        admin = None
    return render_template(
        "drink_details.html",
        drink=result,
        stores=stores,
        category=category,
        reviews=reviews,
        admin=admin,
        score=score,
    )


@app.route("/drink/delete/<int:drink_id>")
def delete_drink(drink_id):
    if users.is_admin(session["username"]):
        drinks.delete(drink_id)
    return redirect("/drinks")


@app.route("/review/delete/<int:review_id>")
def delete_review(review_id):
    if users.is_admin(session["username"]):
        drinks.delete_review(review_id)
    return redirect("/drinks")


@app.route("/profile/delete/<int:user_id>")
def delete_user(user_id):
    if users.is_admin(session["username"]):
        users.delete_user(user_id)
    return redirect("/profiles")


@app.route("/drink/add")
def add_drink():
    categories = drinks.category_list()
    stores = drinks.store_list()
    return render_template("add_drink.html", categories=categories, stores=stores)


@app.route("/drink/create", methods=["POST"])
def create_drink():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    categories = drinks.category_list()
    stores = drinks.store_list()
    name = request.form["drink_name"]
    percentage = request.form["drink_percentage"]
    category_id = request.form["drink_category"]
    store_ids = request.form.getlist("drink_store")
    price = request.form["drink_price"]

    if len(name) > 30:
        return render_template(
            "add_drink.html",
            message="Beverage name too long!",
            categories=categories,
            stores=stores,
        )
    elif float(percentage) > 100:
        return render_template(
            "add_drink.html",
            message="The percentage cannot be that big!",
            categories=categories,
            stores=stores,
        )
    elif float(price) > 100000:
        return render_template(
            "add_drink.html",
            message="That price is way too big!",
            categories=categories,
            stores=stores,
        )
    else:
        add = drinks.create_drink(name, percentage, category_id, store_ids, price)

    if add == 0:
        return redirect("/drinks")
    else:
        return render_template(
            "add_drink.html",
            message="That beverage already exists!",
            categories=categories,
            stores=stores,
        )


@app.route("/profile/<username>")
def profile(username):
    user_id = users.user_check(username).id
    reviews = drinks.list_user_reviews(user_id)
    admin_value = None
    try:
        if username == session["username"]:
            if users.check_admin() == False:
                admin_value = True
    except:
        admin_value = None
    return render_template(
        "profile.html", username=username, reviews=reviews, admin=admin_value
    )


@app.route("/profiles")
def profiles():
    all_profiles = users.list_profiles()
    try:
        admin = users.is_admin(session["username"])
    except:
        admin = None
    return render_template("profiles.html", profiles=all_profiles, admin=admin)


@app.route("/profiles_s", methods=["GET"])
def profile_search():
    s_filter = request.args["s_filter"]
    if s_filter:
        profiles = users.search_profiles(s_filter)
    else:
        profiles = users.list_profiles()
    return render_template("profiles.html", profiles=profiles)


@app.route("/review/give/<int:drink_id>", methods=["POST", "GET"])
def give_review(drink_id):
    drink = drinks.drink_name(drink_id)
    return render_template("give_review.html", drink=drink)


@app.route("/review/add/<int:drink_id>", methods=["POST", "GET"])
def add_review(drink_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    review = request.form["review"]
    score = request.form["score"]
    if len(review) > 200:
        drink = drinks.drink_name(drink_id)
        return render_template(
            "give_review.html", drink=drink, message="That review is too long!"
        )
    else:
        drinks.create_new_review(drink_id, session["username"], review, score)
        return drink_page(drink_id)


@app.route("/admin", methods=["POST", "GET"])
def admin_create():
    username = session["username"]
    password = request.form["admin_password"]
    if password == "Khakapyly":
        users.create_admin(username)
    redir = str("/profile/" + username)
    return redirect(redir)
