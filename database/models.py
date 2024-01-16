from app import db


class Users(db.Model):
    userid = db.Column("UserID", db.String(20), primary_key=True)
    email = db.Column("EmailID", db.String(100))
    username = db.Column("Name", db.String(100))
    password = db.Column("Password", db.String(20))

    def __init__(self, userid, email, username, password):
        self.userid = userid
        self.email = email
        self.username = username
        self.password = password


class AboutMe(db.Model):
    userid = db.Column("UserID", db.String(20), primary_key=True)
    email = db.Column("EmailID", db.String(100))
    summary = db.Column("Summary", db.String(64000))
    about = db.Column("About", db.String(16000000))
    company = db.Column("Company", db.String(100))
    dpfile = db.Column("DPFile", db.String(500))
    designation = db.Column("Designation", db.String(100))
    dob = db.Column("DOB", db.String(10))
    phone = db.Column("Phone", db.String(15))
    city = db.Column("City", db.String(100))
    availability = db.Column("Availability", db.Integer())
    website = db.Column("Website", db.String(100))

    def __init__(self, userid, email, summary, about, company, dpfile, designation, dob, phone, city, availability, website):
        self.userid = userid
        self.email = email
        self.summary = summary
        self.about = about
        self.company = company
        self.dpfile = dpfile
        self.designation = designation
        self.dob = dob
        self.phone = phone
        self.city = city
        self.availability = availability
        self.website = website


if __name__ == "__main__":
    # Run this file directly to create the database tables.
    db.create_all()