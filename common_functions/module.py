import re
from datetime import date
from functools import wraps
from flask import session, redirect, url_for, flash
from constants.common_constants import USERID, MESSAGE, LOGIN


def calculate_age(dob):
    year, month, day = list(map(lambda s: int(s), dob.split("-")))
    birth_date = date(year, month, day)
    today = date.today()
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    return f"{age} years"


def anchorify(url, mailto=False):
    if not mailto:
        link = f"https://{url}" if not url.startswith("http") else url
        return f'<a target="_blank" href="{link}">{url}</a>'
    return f'<a target="_blank" href="mailto:{url}">{url}</a>'


def url_detector(para):
    regex = (
        r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|"
        r"(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    )
    urls = re.findall(regex, para)
    for url in urls:
        para = para.replace(url[0], anchorify(url[0]))
    return para


def check_login(route_func):
    @wraps(route_func)
    def validate():
        userid = session.get(USERID, None)
        if not userid:
            flash("You are not logged in. Please login.", MESSAGE)
            return redirect(url_for(LOGIN))
        return route_func()

    return validate


def dob_format(dob):
    months = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }
    year, month, day = dob.split("-")
    return f"{day} {months[month][:3]}, {year}"
