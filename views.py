from app import app, db
from common_functions.module import *
from flask import session, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import AboutMe, Users
from constants.common_constants import *
from sqlalchemy.exc import OperationalError
import copy
import os
from datetime import timedelta

ABOUTME = {}


@app.route("/register/", methods=[GET_METHOD, POST_METHOD])
def register():
    if request.method == GET_METHOD:
        return render_template(REGISTER_PAGE)
    elif request.method == POST_METHOD:
        userid = request.form[USERNAME]
        email = request.form[EMAIL]
        username = request.form[FULLNAME]
        password = generate_password_hash(request.form[PASSWORD])
        user_exists = Users.query.filter_by(userid=userid).first()
        if not user_exists:
            user = Users(userid=userid, email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash("User registered successfully! Login now!", MESSAGE)
            return redirect(url_for(LOGIN))
        else:
            flash("User already exists!", MESSAGE)
            return redirect(url_for(REGISTER))


@app.route("/login/", methods=[GET_METHOD, POST_METHOD])
def login():
    if request.method == GET_METHOD:
        return render_template(LOGIN_PAGE)
    elif request.method == POST_METHOD:
        userid = request.form[USERNAME]
        password = request.form[PASSWORD]
        user_exists = Users.query.filter_by(userid=userid).first()
        if user_exists:
            if check_password_hash(user_exists.password, password):
                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes=5)
                session.modified = True
                session[USERID] = userid
                session[USERNAME] = user_exists.username
            else:
                flash("Credentials don't match.", MESSAGE)
                return redirect(url_for(LOGIN))
        else:
            flash("Invalid user", MESSAGE)
            return redirect(url_for(LOGIN))

        return redirect(url_for(HOME))


@app.route("/logout/")
def logout():
    if session.get(USERID, None):
        del session[USERID]
        del session[USERNAME]
        flash("You've been successfully logged out!", MESSAGE)
    else:
        flash("You've already been logged out!", MESSAGE)
    return redirect(url_for(LOGIN))


@app.route("/")
@app.route("/home/")
@check_login
def home_page():
    userid = session[USERID]
    username = session[USERNAME]
    try:
        query = AboutMe.query.filter_by(userid=userid).first()
        if not query:
            return render_template(ALT_INDEX, name=username.title())
        aboutme = query.summary
    except OperationalError:
        return render_template(ALT_INDEX, name=username.title())
    return render_template(INDEX_PAGE, name=username.title(), aboutme=aboutme)


@app.route("/about/")
@check_login
def about_me():
    userid = session[USERID]
    user_details = AboutMe.query.filter_by(userid=userid).first()

    about_fields = dict()
    about_fields[EMAIL] = anchorify(user_details.email, mailto=True)
    about_fields[SUMMARY] = user_details.summary
    about_fields[ABOUT] = urldetector(user_details.about)
    about_fields[COMPANY] = user_details.company
    about_fields[DPFILE] = user_details.dpfile
    if not about_fields[DPFILE]:
        about_fields[DPFILE] = PROFILE_PIC
    about_fields[DESIGNATION] = user_details.designation
    dob = user_details.dob
    if dob:
        about_fields[DOB] = dobformat(dob)
    else:
        about_fields[DOB] = None
    about_fields[PHONE] = user_details.phone
    about_fields[CITY] = user_details.city
    about_fields[WEBSITE] = anchorify(user_details.website)
    about_fields[AVAILABILITY] = JOB_ACTIVITY.get(user_details.availability)
    if about_fields[DOB]:
        about_fields[AGE] = calculateage(dob)
    else:
        about_fields[AGE] = None
    global ABOUTME
    ABOUTME = about_fields
    return render_template(
        ABOUT_PAGE,
        **about_fields,
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


@app.route("/about/addormodify/", methods=[GET_METHOD, POST_METHOD])
@check_login
def add_or_modify():
    userid = session[USERID]
    user_exists = Users.query.filter_by(userid=userid).first()
    if request.method == GET_METHOD:
        global ABOUTME
        about_fields = copy.deepcopy(ABOUTME)
        if about_fields.get(EMAIL):
            about_fields[EMAIL] = about_fields[EMAIL].split("\"")[4].replace("/a", "").strip("<>")
        if about_fields.get(WEBSITE):
            about_fields[WEBSITE] = about_fields[WEBSITE].split("\"")[4].replace("/a", "").strip("<>")
        return render_template(MODIFY_PAGE, **about_fields)

    elif request.method == POST_METHOD:
        updateflag = False
        filepath = PIC_PATH
        email = request.form.get(EMAIL)
        if email and email != user_exists.email:
            user_exists.email = email
            db.session.commit()
        summary = request.form.get(SUMMARY)
        about = request.form.get(ABOUT)
        company = request.form.get(COMPANY)
        dpfile = request.files[DPFILE]
        designation = request.form.get(DESIGNATION)
        dob = request.form.get(DOB)
        phone = request.form.get(PHONE)
        city = request.form.get(CITY)
        website = request.form.get(WEBSITE)
        availability = request.form.get(AVAILABILITY)
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
                flash("Details inserted successfully!", MESSAGE)
            else:
                db.session.commit()
                flash("Details updated successfully!", MESSAGE)
            return redirect(url_for(ABOUT_ME))
