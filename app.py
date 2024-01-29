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
    if "user" in session:
        return redirect(url_for("dashboard"))

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
        location_count = locations_count()
        item_count = items_count()
        return redirect(url_for("dashboard", location_count=location_count, item_count=item_count))
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
                    location_count = locations_count()
                    item_count = items_count()
                    return redirect(url_for("dashboard", location_count=location_count, item_count=item_count))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        flash ("You must be logged in")
        return redirect(url_for("login"))

    if session["user"]:
        # get the total number of locations from db
        location_count = locations_count()
        # get the total number of items from db
        item_count = items_count()
        return render_template("dashboard.html", location_count=location_count, item_count=item_count)


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


@app.route("/delete_location/<location_id>")
def delete_location(location_id):
    if "user" not in session:
        flash ("You must be logged in")
        return redirect(url_for("login"))

    location = mongo.db.locations.find_one({"_id": ObjectId(location_id)})
    if not location:
        flash("Location not found")
        return redirect(url_for("get_locations"))

    return render_template("delete_location.html", location=location)


@app.route("/delete_location_confirm/<location_id>", methods=["GET", "POST"])
def delete_location_confirm(location_id):
    if request.method == "POST":
        user_id = get_user_id()
        if request.form.get("delete_all_items"):
            mongo.db.items.delete_many({"location_id": location_id})
        mongo.db.locations.delete_one({"_id": ObjectId(location_id)})

        if request.form.get("delete_all_items"):
            flash("Location and Items Successfully Deleted")
            return redirect(url_for("get_locations"))
        else:
            flash("Location Successfully Deleted")
            return redirect(url_for("get_locations"))

    else:
        flash("Invalid request")
        return redirect(url_for("get_locations"))


@app.route("/get_items_all")
def get_items_all():
    if "user" not in session:
        flash ("You must be logged in")
        return redirect(url_for("login"))
    
    user_id = get_user_id()

    items = list(mongo.db.items.find({"user_id": {'$eq': user_id}}).sort("item_name", 1))
    return render_template("items.html", items=items)


@app.route("/get_items/<location_id>")
def get_items(location_id):
    if "user" not in session:
        flash ("You must be logged in")
        return redirect(url_for("login"))

    location = mongo.db.locations.find_one({"_id": ObjectId(location_id)})
    location_name = location["location_name"]
    items = list(mongo.db.items.find({"location_id": {'$eq': location_id}}).sort("item_name", 1))
    return render_template("items.html", items=items, location_id=location_id, location_name=location_name)


@app.route("/add_item/<location_id>", methods=["GET", "POST"])
def add_item(location_id):
    if "user" not in session:
        flash ("You must be logged in")
        return redirect(url_for("login"))
    
    user_id = get_user_id()
    # For testing purposes
    print(location_id)

    if request.method == "POST":
        location = mongo.db.locations.find_one({"location_name": {'$eq': request.form.get("location_name")}})
        new_location_id = str(location["_id"])
        
        item = {
            "user_id": user_id,
            "location_id": new_location_id,
            "location_name": request.form.get("location_name"),
            "item_name": request.form.get("item_name"),
            "quantity": request.form.get("quantity"),
            "min_quantity": request.form.get("min_quantity"),
            "purchase_date": request.form.get("purchase_date"),
            "expiry_date": request.form.get("expiry_date"),
            "price": request.form.get("price"),
            "note": request.form.get("note")
        }   

        item_name_exist = mongo.db.items.count_documents({"user_id": user_id, "item_name": {'$eq': request.form.get("item_name")}})

        if item_name_exist >= 1:
            flash ("Item already exists")
            return redirect(url_for("add_item", location_id=location_id))

        mongo.db.items.insert_one(item)
        flash("Item Successfully Added")
        return redirect(url_for("get_items", location_id=new_location_id))
    
    locations = mongo.db.locations.find({"user_id": {'$eq': user_id}}).sort("location_name", 1)
    return render_template("add_item.html", locations=locations, location_id=location_id)


@app.route("/edit_item/<location_id>/<item_id>", methods=["GET", "POST"])
def edit_item(location_id,item_id):
    if "user" not in session:
        flash ("You must be logged in")
        return redirect(url_for("login"))
    
    user_id = get_user_id()

    if request.method == "POST":
        location = mongo.db.locations.find_one({"location_name": {'$eq': request.form.get("location_name")}})
        new_location_id = str(location["_id"])

        submit = {
            "user_id": user_id,
            "location_id": new_location_id,
            "location_name": request.form.get("location_name"),
            "item_name": request.form.get("item_name"),
            "quantity": request.form.get("quantity"),
            "min_quantity": request.form.get("min_quantity"),
            "purchase_date": request.form.get("purchase_date"),
            "expiry_date": request.form.get("expiry_date"),
            "price": request.form.get("price"),
            "note": request.form.get("note")
        }

        item = mongo.db.items.find_one({"user_id": user_id, "item_name": {'$eq': request.form.get("item_name")}})
        item_id_check = str(item["_id"])
        
        if item_id == item_id_check:
            mongo.db.items.replace_one({"_id": ObjectId(item_id)}, submit)
            flash("Item Successfully Edited")
            return redirect(url_for("get_items", location_id=new_location_id))
        else:
            flash ("Item already exists")
            return redirect(url_for("edit_item", location_id=new_location_id, item_id=item_id))

    item = mongo.db.items.find_one({"_id": ObjectId(item_id)})
    locations = mongo.db.locations.find({"user_id": {'$eq': user_id}}).sort("location_name", 1)
    return render_template("edit_item.html", location_id=location_id, locations=locations, item=item)


@app.route("/delete_item/<location_id>/<item_id>")
def delete_item(location_id,item_id):
    if "user" not in session:
        flash ("You must be logged in")
        return redirect(url_for("login"))

    item = mongo.db.items.find_one({"_id": ObjectId(item_id)})
    if not item:
        flash("Item not found")
        return redirect(url_for("get_items", location_id=location_id))

    return render_template("delete_item.html", location_id=location_id, item=item)


@app.route("/delete_item_confirm/<location_id>/<item_id>", methods=["GET", "POST"])
def delete_item_confirm(location_id,item_id):
    if request.method == "POST":
        mongo.db.items.delete_one({"_id": ObjectId(item_id)})
        flash("Item Successfully Deleted")
        return redirect(url_for("get_items", location_id=location_id))
    else:
        flash("Invalid request")
        return redirect(url_for("get_items", location_id=location_id))


def get_user_id():
    # Get the current user_id from db
    user = mongo.db.users.find_one({"username": session["user"]})
    # For testing purposes
    print(user)
    user_id = str(user["_id"])
    #For testing purposes
    print(user_id)

    return user_id


def get_location_id(user_id, location_name):
    #Get the location_id from db
    location = mongo.db.locations.find_one({"user_id": user_id, "location_name": {'$eq': location_name}})
    # For testing purposes
    print(location)
    location_id = str(location["_id"])
    #For testing purposes
    print(location_id)

    return location_id


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
