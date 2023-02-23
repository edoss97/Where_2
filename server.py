from flask import (Flask, render_template, request, flash, session,redirect)

from model import connect_to_db, db
from jinja2 import StrictUndefined
import crud

app = Flask(__name__)
app.secret_key = "banana"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def login():
    return render_template('login.html')

@app.route("/homepage")
def homepage():
    logged_in_user_id = session.get("user_id")
    user = crud.get_user_by_user_id(logged_in_user_id)
    username=user.username
    return render_template('homepage.html', username=username)

@app.route('/destination')
def all_destinations():
    destinations = crud.get_destinations()
    
    return render_template('all_destination.html', destinations=destinations)

@app.route('/destination/<destination_id>')
def dest_id(destination_id):
    logged_in_user_id = session.get("user_id")
    destination = crud.get_dest_by_id(destination_id)
    lists=crud.get_list_by_user_id(logged_in_user_id)
    all_ratings=crud.get_avg_rating(destination_id)
    rating_list=[]
    for rating in all_ratings:
        rating_list.append(rating.rating)
    total_rating=sum((rating_list))/(len(rating_list))
    average_rating=round(total_rating,2)
    return render_template("destination_details.html", destination=destination, lists=lists, average_rating=average_rating)

@app.route("/users", methods=["POST"])
def register_user():

    username = request.form.get("username")
    password = request.form.get("password")
    user = crud.get_user_by_username(username)
    if user:
        flash("Cannot create an account with that username. Try again.")
        return redirect("/")
    else:
        user = crud.create_user(username, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    username=user.username
    return render_template("homepage.html", username=username)

@app.route("/login", methods=["POST"])
def process_login():

    username = request.form.get("username")
    password = request.form.get("password")
    user = crud.get_user_by_username(username)
    if user == None:
        print("username failed")
        flash("The username and/or password are incorrect, try again.")
        if user.password != password:
            print("password failed")

            return redirect("/")
    else:
        session["user_id"] = user.user_id
        flash(f"Welcome back, {user.user_id}!")
        username=user.username
        return render_template("homepage.html", username=username)

@app.route("/destination/ratings/<destination_id>", methods=["POST"])
def create_rating(destination_id):

    logged_in_user_id = session.get("user_id")
    rating_score = request.form.get("rating")

    if logged_in_user_id is None:
        flash("You must log in to rate a destination.")
    elif not rating_score:
        flash("Error: you didn't select a score for your rating.")
    else:
        rating = crud.create_rating(logged_in_user_id, destination_id, (rating_score))
        db.session.add(rating)
        db.session.commit()

        flash(f"You rated this  {rating_score} out of 5.")
    return redirect(f"/destination/{destination_id}")



@app.route("/destination/add/<destination_id>", methods=["POST"])
def add_dest_to_list(destination_id):

    logged_in_user_id = session.get("user_id")
    lists=crud.get_list_by_user_id(logged_in_user_id)
    list_id=request.form.get("add_dest")
    destination = crud.get_dest_by_id(destination_id)
    
    new_dest=crud.create_list_dest(list_id,destination_id,logged_in_user_id)
    db.session.add(new_dest)
    db.session.commit()
    return redirect(f"/destination")

@app.route("/list")
def all_lists():

    logged_in_user_id = session.get("user_id")
    lists = crud.get_list_by_user_id(logged_in_user_id)
    return render_template('all_list.html', lists=lists)

@app.route("/list/<list_id>")
def list_id(list_id):
    list = crud.get_list_by_id(list_id)
    dest_list = crud.get_dest_id_by_list_id(list_id)
    destination_id_in_list = []
    destinations = []
    for destination in dest_list:
        destination_id_in_list.append(destination.destination_id)
    for destination in destination_id_in_list:
        full_dest= crud.get_dest_by_id(destination)
        destinations.append(full_dest)
    
    return render_template("list_detail.html", list=list, destinations = destinations)

@app.route("/new_list", methods=["POST"])
def new_list():
    logged_in_user_id = session.get("user_id")
    list_name = request.form.get("list_name")
    new_list= crud.create_list(logged_in_user_id, list_name)
    db.session.add(new_list)
    db.session.commit()
    return redirect(f"/list") 

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="localhost",port = 3001, debug=True)