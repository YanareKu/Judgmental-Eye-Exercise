from flask import Flask, render_template, redirect, request, flash, session as flask_session
import model

app = Flask(__name__)
app.secret_key = 'weeeeeeeeeeeeeeeeeeeeeesecreeeetssss!!!!'

@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("index.html")

@app.route("/login_route")
def login_page():
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


if __name__ == "__main__":
    app.run(debug = True)