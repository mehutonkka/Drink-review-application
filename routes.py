from app import app
import users
import drinks
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

#Functionality to login to the website and to be redirected to the home page
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    result = users.login(username, password)
    if result == 1:
        return render_template("index.html", login_message='Incorrect username!')
    elif result == 0:
        session["username"] = username
        return redirect("/home_page")
    else:
        return render_template("index.html", login_message='Incorrect username/password!')


#Functionality to signup/create a new user and be redirected to the home page
@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    password1 = request.form["password1"]
    session["username"] = username
    result = users.signup(username, password, password1)
    if result == 0:
        return redirect("/home_page")
    elif result == 1:
        return render_template("index.html", signup_message="The two passwords do not match!")
    else:
        return render_template("index.html", signup_message="That username is already in use!")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/home_page", methods=["GET", "POST"])
def home_page():
    top10 = drinks.top_10_drinks()
    top5 = users.top5_users()
    return render_template("home_page.html", top10=top10, top5=top5)



    
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
        if category_id!="0":
            result = drinks.list_search_category(s_filter, category_id)
        else:
            result = drinks.list_search(s_filter)
    else:
        if category_id:
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
    return render_template("drink_details.html", drink=result, stores=stores, category=category, reviews=reviews)



@app.route("/drink/add")
def add_drink():
    categories = drinks.category_list()
    stores = drinks.store_list()
    return render_template("add_drink.html", categories=categories, stores=stores)

@app.route("/drink/create", methods=["POST"])
def create_drink():
    categories = drinks.category_list()
    stores = drinks.store_list()
    name = request.form["drink_name"]
    percentage = request.form["drink_percentage"]
    category_id = request.form["drink_category"]
    store_ids = request.form.getlist("drink_store")
    price = request.form["drink_price"]
    add = drinks.create_drink(name, percentage, category_id, store_ids, price)
    if add == 0:
        return redirect("/home_page")
    else:
        return render_template("add_drink.html", message="That beverage already exists!", categories=categories, stores=stores)
    
@app.route("/profile/<username>")
def profile(username):
    user_id = users.user_check(username).id
    reviews = drinks.list_user_reviews(user_id)
    return render_template("profile.html", username=username, reviews=reviews)

@app.route("/profiles")
def profiles():
    all_profiles = users.list_profiles()
    return render_template("profiles.html", profiles=all_profiles)


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
    review = request.form["review"]
    score = request.form["score"]
    drinks.create_new_review(drink_id, session["username"], review, score)
    return drink_page(drink_id)



