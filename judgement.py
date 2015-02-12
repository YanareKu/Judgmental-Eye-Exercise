from flask import Flask, render_template, redirect, request, flash, g, session as flask_session
import model

app = Flask(__name__)
app.secret_key = 'weeeeeeeeeeeeeeeeeeeeeesecreeeetssss!!!!'

@app.before_request
def global_variables():
    g.user_id = flask_session["user"]["id"]

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
    ## movie_list= list of movie objects

    movie_rating_list=[]
    for movie in movie_list:
        rating = model.get_users_rating(movie.id, g.user_id)
        movie_rating_list.append((movie, rating))

    return render_template("/movie_list.html", movie_list=movie_rating_list)

@app.route("/rate_me/<int:id>")
def create_ratings(id):
    movie_id = id
    movie = model.get_movie_name_by_movie_id(movie_id)
    return render_template("rate_me.html", movie=movie)

@app.route("/add_rating/<int:id>", methods = ["POST"])
def add_rating(id):
    rating = request.form.get("rating")
    user_id = g.user_id
    movie_id = id
    movie_object= model.get_movie_name_by_movie_id(movie_id)
    movie_name = movie_object.name
    print model.get_users_rating(movie_id, user_id), "********************"
    if model.get_users_rating(movie_id, user_id) == "Not rated":
        model.insert_rating(user_id, movie_id, rating)
        flash("The rank %s has been added to the movie %s!" % (rating, movie_name)) 
        return redirect("/movies")
    else:
        model.update_existing_rating(user_id, movie_id, rating)
        flash("The rank for movie %s has been updated to %s!" % (movie_name, rating))         
        return redirect("/movies")



if __name__ == "__main__":
    app.run(debug = True)