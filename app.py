from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from constants.common_constants import (
    APPLICATION_SECRET_KEY,
    DATABASE_URI,
    SECRET_KEY,
    SQLITE_DATABASE_FILE,
    TRACK_MODIFICATION,
)

app = Flask(__name__)
app.config[SECRET_KEY] = APPLICATION_SECRET_KEY
app.config[DATABASE_URI] = SQLITE_DATABASE_FILE
app.config[TRACK_MODIFICATION] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


if __name__ == "__main__":
    from views import *

    app.run(debug=True)  # ssl_context="adhoc" will enable https for test
