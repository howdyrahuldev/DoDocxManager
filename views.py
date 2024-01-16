from app import app, db
from common_functions.module import *
from flask import session, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import AboutMe, Users
from sqlalchemy.exc import OperationalError
import copy
import os
from datetime import timedelta

ABOUT = {}


@app.route("/")
@app.route("/home/")
@check_login
def homepage():
    userid = session["userid"]
    username = session["username"]
    try:
        query = AboutMe.query.filter_by(userid=userid).first()
        if not query:
            return render_template("index2.html", name=username.title())
        aboutme = query.summary
    except OperationalError:
        return render_template("index2.html", name=username.title())
    return render_template("index.html", name=username.title(), aboutme=aboutme)


@app.route("/about/")
@check_login
def aboutme():
    userid = session["userid"]
    job_availability = {
        0: "Not now",
        1: "Yes, actively",
        2: "Not actively, but up for an opportunity"
    }
    user_details = AboutMe.query.filter_by(userid=userid).first()
    aboutparams = {}
    aboutparams["email"] = anchorify(user_details.email, mailto=True)
    aboutparams["summary"] = user_details.summary
    aboutparams["about"] = urldetector(user_details.about)
    aboutparams["company"] = user_details.company
    aboutparams["dpfile"] = user_details.dpfile
    if not aboutparams["dpfile"]:
        aboutparams["dpfile"] = "profile_avatar.jpg"
    aboutparams["designation"] = user_details.designation
    dob = user_details.dob
    if dob:
        aboutparams["dob"] = dobformat(dob)
    else:
        aboutparams["dob"] = None
    aboutparams["phone"] = user_details.phone
    aboutparams["city"] = user_details.city
    aboutparams["website"] = anchorify(user_details.website)
    aboutparams["availability"] = job_availability.get(user_details.availability)
    if aboutparams["dob"]:
        aboutparams["age"] = calculateage(dob)
    else:
        aboutparams["age"] = None
    global ABOUT
    ABOUT = aboutparams
    return render_template(
        "about.html",
        **aboutparams,
        skilldesc="Web/Application Developer, who has working experience with Data Engineering and DevOps automation and pipelines.",
        skill1="Python",
        progress1="100",
        skill2="Flask",
        progress2="80",
        skill3="DevOps",
        progress3="80",
        skill4="AWS",
        progress4="60",
        skill5="Linux",
        progress5="80",
        skill6="SQL",
        progress6="60",
    )


@app.route("/about/addormodify/", methods=["GET", "POST"])
@check_login
def addormodify():
    userid = session["userid"]
    user_exists = Users.query.filter_by(userid=userid).first()
    if request.method == "GET":
        global ABOUT
        about_user = copy.deepcopy(ABOUT)
        if about_user.get("email"):
            about_user["email"] = about_user["email"].split("\"")[4].replace("/a", "").strip("<>")
        if about_user.get("website"):
            about_user["website"] = about_user["website"].split("\"")[4].replace("/a", "").strip("<>")
        return render_template("modifyprofile.html", **about_user)
    elif request.method == "POST":
        updateflag = False
        filepath = "./static/profile_avatars/"
        email = request.form.get("email")
        if email and email != user_exists.email:
            user_exists.email = email
            db.session.commit()
        summary = request.form.get("summary")
        about = request.form.get("about")
        company = request.form.get("company")
        dpfile = request.files["dpfile"]
        designation = request.form.get("designation")
        dob = request.form.get("dob")
        phone = request.form.get("phone")
        city = request.form.get("city")
        website = request.form.get("website")
        availability = request.form.get("availability")
        try:
            user_details = AboutMe.query.filter_by(userid=userid).first()
            if user_details:
                updateflag = True
                if email:
                    user_details.email = email
                else:
                    if not user_details.email:
                        user_details.email = user_exists.email
                if summary:
                    user_details.summary = summary
                if about:
                    user_details.about = about
                if company:
                    user_details.company = company
                if dpfile:
                    previousfile = None
                    if user_details.dpfile:
                        previousfile = f"{filepath}{user_details.dpfile}"

                    if previousfile and os.path.exists(previousfile):
                        os.remove(previousfile)

                    dpfilename = f"{userid}.{dpfile.filename.rsplit('.', 1)[-1]}"
                    dpfile.save(f"{filepath}{dpfilename}")
                    user_details.dpfile = dpfilename
                if designation:
                    user_details.designation = designation
                if dob:
                    user_details.dob = dob
                if phone:
                    user_details.phone = phone
                if city:
                    user_details.city = city
                if website:
                    user_details.website = website
                if availability:
                    availability = int(availability)
                    user_details.availability = availability
        except OperationalError as e:
            print("Operation exception happened", e)
        finally:
            if not updateflag:
                aboutme = AboutMe(
                            userid=userid,
                            email=email,
                            summary=summary,
                            about=about,
                            company=company,
                            dpfile=dpfile.filename,
                            designation=designation,
                            dob=dob,
                            phone=phone,
                            city=city,
                            website=website,
                            availability=availability,
                )
                db.session.add(aboutme)
                db.session.commit()
                flash("Details inserted successfully!", "message")
            else:
                db.session.commit()
                flash("Details updated successfully!", "message")
            return redirect(url_for("aboutme"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        userid = request.form["username"]
        password = request.form["password"]
        user_exists = Users.query.filter_by(userid=userid).first()
        if user_exists:
            if check_password_hash(user_exists.password, password):
                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes=5)
                session.modified = True
                session["userid"] = userid
                session["username"] = user_exists.username
            else:
                flash("Credentials don't match.", "message")
                return redirect(url_for("login"))
        else:
            flash("Invalid user", "message")
            return redirect(url_for("login"))

        return redirect(url_for("homepage"))


@app.route("/logout/")
def logout():
    if session.get("userid", None):
        del session["userid"]
        del session["username"]
        flash("You've been successfully logged out!", "message")
    else:
        flash("You've already been logged out!", "message")
    return redirect(url_for("login"))


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        userid = request.form["username"]
        email = request.form["email"]
        username = request.form["fullname"]
        password = generate_password_hash(request.form["password"])
        user_exists = Users.query.filter_by(userid=userid).first()
        if not user_exists:
            user = Users(userid=userid, email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash("User registered successfully! Login now!", "message")
            return redirect(url_for("login"))
        else:
            flash("User already exists!", "message")
            return redirect(url_for("register"))