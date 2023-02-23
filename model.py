from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class User(db.Model):
    __tablename__= "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f'<User user_id={self.user_id} username= {self.username}>'

class Destination(db.Model):
    __tablename__= "destinations"

    destination_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    destination_name = db.Column(db.String, unique=True)
    destination_url = db.Column(db.String)
    destination_description = db.Column(db.String)

    def __repr__(self):
        return f'<Destination destination_id={self.destination_id} destination_name= {self.destination_name} destination_url= {self.destination_url} destination_description={self.destination_description}'

class Rating(db.Model):
    __tablename__= "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.destination_id"))
    rating = db.Column(db.Float)

    def __repr__(self):
        return f'<Rating rating_id={self.rating} user_id= {self.user_id} destination_id= {self.destination_id} rating={self.rating}>'

class List(db.Model):
    __tablename__ = "lists"

    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    list_name = db.Column(db.String)

    def __repr__(self):
        return f'<List lists_id={self.list_id} list_name={self.list_name}'

class List_Dest(db.Model):
    __tablename__ = "list_dest"

    list_dest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.destination_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):
        return f'<List_Dest list_dest_id={self.list_dest_id} list_id={self.list_id} destination_id = {self.destination_id} user_id = {self.user_id}'


def connect_to_db(flask_app, db_uri=os.environ["POSTGRES_URI"], echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app
    connect_to_db(app)