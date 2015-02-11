from flask import Flask, render_template, redirect, request, flash
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
    print user
#need to write logic on checking email, password, and logging in!!
    if user== None: 
        return "ERMAGERD!"
    elif user.email == email:
        return "IS THIS WORKING?!"



@app.route("/signup")
def signup():
    return render_template("signup.html")




if __name__ == "__main__":
    app.run(debug = True)