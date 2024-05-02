from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv


app.secret_key = getenv("SECRET_KEY")

#To start this web app with flask remove the '#' on the next row if it is there. 
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")#.replace("://", "ql://", 1)
db = SQLAlchemy(app)


