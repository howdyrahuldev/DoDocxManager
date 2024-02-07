# Application Configuration Constants

SECRET_KEY = "SECRET_KEY"
DATABASE_URI = "SQLALCHEMY_DATABASE_URI"
TRACK_MODIFICATION = "SQLALCHEMY_TRACK_MODIFICATIONS"
APPLICATION_SECRET_KEY = "-fA2915AGHcgjROd4cym1meUYEI"
SQLITE_DATABASE_FILE = "sqlite:///myappdb.db"


# HTTP Methods
GET_METHOD = "GET"
POST_METHOD = "POST"


# Generic Keywords
MESSAGE = "message"
LOGIN = "login"
REGISTER = "register"
HOME = "home_page"
ABOUT_ME = "about_me"
HREF = "href"


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
JOB_ACTIVITY = {
    0: "Not now",
    1: "Yes, actively",
    2: "Not actively, but up for an opportunity",
}
DEFAULT_USER_DETAILS = {
                    EMAIL: "Add your email address.",
                    SUMMARY: "Add profile summary e.g who you are, what you love to do, what is your future goals etc.",
                    ABOUT: "Add about yourself.",
                    COMPANY: "Add company name.",
                    DPFILE: None,
                    DESIGNATION: "Add your job title.",
                    DOB: "Add your birthday.",
                    PHONE: "Add phone number.",
                    CITY: "Add city.",
                    WEBSITE: "Add your website address.",
                    AVAILABILITY: "Add your choice.",
                    AGE: "Add your birthday.",
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
