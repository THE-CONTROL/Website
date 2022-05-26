from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from .models import Company, Employee
from . import db
import os
from werkzeug.utils import secure_filename

views = Blueprint("views", __name__)

ALLOWED_EXTENSIONS = set(["jpg", "png", "jpeg"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route("/profile")
@login_required
def profile():
    if current_user.image == "":
        image_file = url_for("static", filename="img/" + "default.jpg")
    else:
        image_file = url_for("static", filename="img/" + current_user.image)
    return render_template("profile.html", company=current_user, image_file=image_file)


@views.route("/update_profile/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
    company = Company.query.get_or_404(id)
    if request.method == "POST":
        company.company_name = request.form.get("company_name")
        company.description = request.form.get("description")
        if "file" not in request.files:
            company.image = company.image
        else:
            file = request.files["file"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join("control/static/img/", filename))
                company.image = filename
            elif file and not allowed_file(file.filename):
                flash("Image type can only be .jpg, .png, .jpeg!", category="error")
                return render_template("update.html", company=current_user)
            else:
                company.image = company.image

        if len(company.company_name) < 2:
            flash("Company name must be greater than 1 character!", category="error")
            return render_template("update.html", company=current_user)
        elif len(company.description) < 10:
            flash("Description must be greater than 9 characters!", category="error")
            return render_template("update.html", company=current_user)
        else:
            db.session.commit()
            flash("Account Updated!", category="success")
            return redirect(url_for("views.profile"))
    return render_template("update.html", company=current_user)


@views.route("/employees")
@login_required
def employees():
    return render_template("employees.html", company=current_user)


@views.route("/addemploy", methods=["GET", "POST"])
@login_required
def addemploy():
    if request.method == "POST":
        employee_name = request.form.get("employee_name")
        job_description = request.form.get("job_description")
        gender = request.form.get("gender")
        if "file" not in request.files:
            image = ""
        else:
            file = request.files["file"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join("control/static/img/", filename))
                image = url_for("static", filename="img/" + filename)
            elif file and not allowed_file(file.filename):
                flash("Image type can only be .jpg, .png, .jpeg!", category="error")
                return render_template("addemploy.html", company=current_user)
            else:
                if gender == "female":
                    image = url_for("static", filename="img/" + "female.jpg")
                elif gender == "male":
                    image = url_for("static", filename="img/" + "male.jpeg")

        if len(employee_name) < 2:
            flash("Employee name must be greater than 1 character!", category="error")
            return render_template("addemploy.html", company=current_user)
        elif len(job_description) < 2:
            flash("Job description must be greater than 1 character!", category="error")
            return render_template("addemploy.html", company=current_user)
        else:
            new_employee = Employee(employee_name=employee_name, job_description=job_description, gender=gender, image=image, company_id=current_user.id)
            db.session.add(new_employee)
            db.session.commit()
            flash("Employee added!", category="success")
            return redirect(url_for("views.employees"))
    else:
        return render_template("addemploy.html", company=current_user)


@views.route("/update_employ/<int:id>", methods=["GET", "POST"])
@login_required
def update_employ(id):
    employee = Employee.query.get_or_404(id)
    if request.method == "POST":
        if employee.company_id == current_user.id:
            employee.employee_name = request.form.get("employee_name")
            employee.job_description = request.form.get("job_description")
            employee.gender = request.form.get("gender")
            if "file" not in request.files:
                employee.image = ""
            else:
                file = request.files["file"]
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join("control/static/img/", filename))
                    employee.image = url_for("static", filename="img/" + filename)
                elif file and not allowed_file(file.filename):
                    flash("Image type can only be .jpg, .png, .jpeg!", category="error")
                    return render_template("update_employ.html", company=current_user)
                elif employee.image == url_for("static", filename="img/" + "female.jpg") or employee.image == url_for("static", filename="img/" + "male.jpeg"):
                    if employee.gender == "female":
                        employee.image = url_for("static", filename="img/" + "female.jpg")
                    elif employee.gender == "male":
                        employee.image = url_for("static", filename="img/" + "male.jpeg")
                else:
                    employee.image = employee.image

            if len(employee.employee_name) < 2:
                flash("Employee name must be greater than 1 character!", category="error")
                return render_template("update_employ.html", company=current_user)
            elif len(employee.job_description) < 2:
                flash("Job description must be greater than 1 character!", category="error")
                return render_template("update_employ.html", company=current_user)
            else:
                db.session.commit()
                flash("Employee updated!", category="success")
                return redirect(url_for("views.employees"))
    else:
        return render_template("update_employ.html", company=current_user, employee=employee)


@views.route("/delete_employ/<int:id>")
@login_required
def delete(id):
    employee = Employee.query.get_or_404(id)
    if employee.company_id == current_user.id:
        db.session.delete(employee)
        db.session.commit()
        flash("Employee removed!")
        return redirect(url_for("views.employees"))
