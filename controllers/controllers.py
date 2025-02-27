from flask import Flask,render_template,request,url_for,redirect
from models.models import *
from flask import current_app as app

#starting route
@app.route("/")
def home():
    return render_template("index.html")

#admin login route
@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")

        usr=User.query.filter_by(email=uname,password=pwd).first()
        if usr and usr.role==0: #Existed and admin
            return redirect(url_for("admin_dashboard"))
        elif usr and usr.role==1: #Existed and user
            return redirect(url_for("user_dashboard"))
        else:
            return render_template("login.html",msg="Invalid email or password. Please try again.")


    return render_template("login.html",msg="")

@app.route("/register",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        full_name=request.form.get("full_name")
        qualification=request.form.get("qualification")
     
        usr=User.query.filter_by(email=uname).first()
        if usr:
            return render_template("register.html",msg="This email is already registered. Please log in or use a different email.")

        new_usr=User(email=uname,password=pwd,full_name=full_name,qualification=qualification)
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html",msg1="Thank you for registering! Try logging in now.")

    return render_template("register.html")

#common route for admin
@app.route("/admin")
def admin_dashboard():

    return render_template("admin_dashboard.html")

#common route for user
@app.route("/user")
def user_dashboard():

    return render_template("user_dashboard.html")



