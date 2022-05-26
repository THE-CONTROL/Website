from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Company
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename

auth = Blueprint("auth", __name__)

ALLOWED_EXTENSIONS = set(["jpg", "png", "jpeg"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route("/", methods=["GET", "POST"])
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        company_name = request.form.get("company_name")
        password = request.form.get("password")

        company = Company.query.filter_by(company_name=company_name).first()
        if company:
            if check_password_hash(company.password, password):
                flash("Login successful!", category="success")
                login_user(company, remember=True)
                return redirect(url_for("views.profile"))
            else:
                flash("Incorrect password, try again!", category="error")
                return render_template("login.html", company=current_user)
        else:
            flash("Company account does not exist, sign up first!", category="error")
            return render_template("login.html", company=current_user)
    else:
        return render_template("login.html", company=current_user)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        company_name = request.form.get("company_name")
        description = request.form.get("description")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        if "file" not in request.files:
            image = ""
        else:
            file = request.files["file"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join("control/static/img/", filename))
                image = filename
            elif file and not allowed_file(file.filename):
                flash("Image type can only be .jpg, .png, .jpeg!", category="error")
                return render_template("signup.html", company=current_user)
            else:
                image = ""

        company1 = Company.query.filter_by(company_name=company_name).first()

        if company1:
            flash("Company account already exist, try a different name!", category="error")
            return render_template("signup.html", company=current_user)
        elif len(company_name) < 2:
            flash("Company name must be greater than 1 character!", category="error")
            return render_template("signup.html", company=current_user)
        elif len(description) < 10:
            flash("Description must be greater than 9 characters!", category="error")
            return render_template("signup.html", company=current_user)
        elif len(password1) < 7:
            flash("Password must be greater than 6 characters!", category="error")
            return render_template("signup.html", company=current_user)
        elif password1 != password2:
            flash("Passwords don't match!", category="error")
            return render_template("signup.html", company=current_user)
        else:
            new_company = Company(company_name=company_name, image=image, description=description,
                                  password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_company)
            db.session.commit()
            login_user(new_company, remember=True)
            flash("Account Created", category="success")
            return redirect(url_for("views.profile"))

    else:
        return render_template("signup.html", company=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
