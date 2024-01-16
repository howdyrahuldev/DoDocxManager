from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from constants.common_constants import SECRET_KEY, DATABASE_URI, TRACK_MODIFICATION

app = Flask(__name__)
app.config[SECRET_KEY] = "-fA2915AGHcgjROd4cym1meUYEI"
app.config[DATABASE_URI] = "sqlite:///myappdb.db"
app.config[TRACK_MODIFICATION] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


if __name__ == "__main__":
    from views import *
    app.run(debug=True)
