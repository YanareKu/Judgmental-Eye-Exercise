from flask import Flask, render_template, redirect, request, flash, session as flask_session
import model

app = Flask(__name__)
app.secret_key = 'weeeeeeeeeeeeeeeeeeeeeesecreeeetssss!!!!'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login_route")
def login_page():
    if "user" in flask_session:
        return redirect("/movies")
    else:
        return render_template("login.html")

@app.route("/verify_user", methods=["POST"])
def verify_user():
    email= request.form.get("email")
    password= request.form.get("password")

    user = model.get_user_by_email(email)

    if user== None: 
        flash("No user found with that email address.")
        return redirect("/login_route")
    else:
        if user.password == password:
            flask_session["user"]={"email":user.email,"id":user.id}
            flash("Login successful!")
            return redirect("/movies")
        else:
            flash("Email or Password combination do not match our records.")
            return redirect("/login_route")


@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/confirmation", methods=["POST"])
def confirm_signup():
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

    user = model.get_user_by_email(email)

    if user == None:
        model.add_user_to_db(email, password, age, zipcode)
        flash("Please login using your new user information.")
        return redirect("/login_route")
    else:
        flash("This email is already registered to a user")
        return redirect("/signup")

@app.route("/movies")
def display_movie_page():
    return render_template("movie_home.html")

@app.route("/user_list")
def display_user_list():
    user_list = model.session.query(model.User).limit(20).all()
    return render_template("user_list.html", users=user_list)

@app.route("/user_rating/<int:id>")
def show_rating(id):
    """This page shows the ratings of the selected user."""
    ratings_with_movies = model.get_movie_names_and_ratings_by_user_id(id)
    print ratings_with_movies
    return render_template("user_rating.html", ratings_with_movies=ratings_with_movies)

@app.route("/search_list")
def find_movie():

    title = request.args.get("search_box")

    movie_list=model.get_movie_rating_by_movie_name(title)

    return render_template("/movie_list.html", movie_list=movie_list)

if __name__ == "__main__":
    app.run(debug = True)