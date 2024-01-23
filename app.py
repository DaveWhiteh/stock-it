import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "firstname": request.form.get("firstname").lower(),
            "lastname": request.form.get("lastname").lower(),
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        locations = locations_count()
        items = items_count()
        return redirect(url_for("dashboard", locations=locations, items=items))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(request.form.get("username")))
                    locations = locations_count()
                    items = items_count()
                    return redirect(url_for("dashboard", locations=locations, items=items))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard/<locations>/<items>", methods=["GET", "POST"])
def dashboard(locations,items):
    if "user" not in session:
        flash ("You must be logged in")

    # get the total number of locations from db
    locations = locations_count()
    # get the total number of items from db
    items = items_count()

    if session["user"]:
        return render_template("dashboard.html", locations=locations, items=items)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/get_locations")
def get_locations():
    if "user" not in session:
        flash ("You must be logged in")
        return redirect(url_for("login"))

    user_id = get_user_id()

    locations = list(mongo.db.locations.find({"user_id": {'$eq': user_id}}).sort("location_name", 1))
    return render_template("locations.html", locations=locations)


@app.route("/add_location", methods=["GET", "POST"])
def add_location():
    if "user" not in session:
        flash ("You must be logged in")
        return redirect(url_for("login"))

    if request.method == "POST":
        user_id = get_user_id()
        location = {
            "user_id": user_id,
            "location_name": request.form.get("location_name")
        }

        location_name_exist = mongo.db.locations.count_documents({"user_id": user_id, "location_name": {'$eq': request.form.get("location_name")}})

        if location_name_exist >= 1:
            flash ("Location already exists")
            return redirect(url_for("add_location"))

        mongo.db.locations.insert_one(location)
        flash("Location Successfully Added")
        return redirect(url_for("get_locations"))

    return render_template("add_location.html")


@app.route("/edit_location/<location_id>", methods=["GET", "POST"])
def edit_location(location_id):
    if "user" not in session:
        flash ("You must be logged in")
        return redirect(url_for("login"))

    if request.method == "POST":
        user_id = get_user_id()
        submit = {
            "user_id": user_id,
            "location_name": request.form.get("location_name")
        }

        location_name_exist = mongo.db.locations.count_documents({"user_id": user_id, "location_name": {'$eq': request.form.get("location_name")}})

        if location_name_exist >= 1:
            flash ("Location already exists")
            return redirect(url_for("edit_location", location_id=location_id))

        mongo.db.locations.replace_one({"_id": ObjectId(location_id)}, submit)
        flash("Location Successfully Edited")
        return redirect(url_for("get_locations"))

    location = mongo.db.locations.find_one({"_id": ObjectId(location_id)})
    return render_template("edit_location.html", location=location)


@app.route("/get_items")
def get_items():
    items = list(mongo.db.items.find())
    return render_template("items.html", items=items)


def get_user_id():
    # Get the current user_id from db
    user = mongo.db.users.find_one({"username": session["user"]})
    # For testing purposes
    print(user)
    user_id = str(user["_id"])
    #For testing purposes
    print(user_id)

    return user_id


def locations_count():
    # Get the current user_id from db
    user_id = get_user_id()

    # Get the count of the locations from db
    count = mongo.db.locations.count_documents({"user_id": user_id})
    # For testing purposes
    print(count)

    return count


def items_count():
    # Get the current user_id from db
    user_id = get_user_id()

    # Get the count of the locations from db
    count = mongo.db.items.count_documents({"user_id": user_id})
    # For testing purposes
    print(count)

    return count


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
