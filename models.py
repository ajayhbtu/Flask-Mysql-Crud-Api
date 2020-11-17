from db_config import db

# User Model
class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.String(100), nullable=False)
    lName = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # for returning the string representation of user object
    def __repr__(self):
        return f"User(id = {id}, fName = {fName}, lName = {lName}, email = {email})"