# auth.py
from flask import Blueprint, render_template, request, redirect, session, url_for

auth_bp = Blueprint("auth", __name__, template_folder="templates")

# Simple demo user (replace with secure DB integration or Firebase in production)
DEMO_USER = {
    "username": "admin",
    "password": "neurosim123"
}

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == DEMO_USER["username"] and password == DEMO_USER["password"]:
            session["user"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))
