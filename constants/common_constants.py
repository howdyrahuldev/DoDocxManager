# Application Configuration Constants

SECRET_KEY = "SECRET_KEY"
DATABASE_URI = "SQLALCHEMY_DATABASE_URI"
TRACK_MODIFICATION = "SQLALCHEMY_TRACK_MODIFICATIONS"


# HTTP Methods
GET_METHOD = "GET"
POST_METHOD = "POST"


# Generic Keywords
MESSAGE = "message"
LOGIN = "login"
REGISTER = "register"
HOME = "home_page"
ABOUT_ME = "about_me"


# User Credentials
USERID = "userid"
USERNAME = "username"
FULLNAME = "fullname"
PASSWORD = "password"
EMAIL = "email"
SUMMARY = "summary"
ABOUT = "about"
COMPANY = "company"
DPFILE = "dpfile"
DESIGNATION = "designation"
DOB = "dob"
PHONE = "phone"
CITY = "city"
WEBSITE = "website"
AVAILABILITY = "availability"
AGE = "age"
JOB_ACTIVITY = \
    {
        0: "Not now",
        1: "Yes, actively",
        2: "Not actively, but up for an opportunity"
    }


# Pages and Avatar Constants
PROFILE_PIC = "profile_avatar.jpg"
PIC_PATH = "./static/profile_avatars/"
LOGIN_PAGE = "login.html"
REGISTER_PAGE = "register.html"
INDEX_PAGE = "index.html"
ALT_INDEX = "index2.html"
ABOUT_PAGE = "about.html"
MODIFY_PAGE = "modifyprofile.html"
