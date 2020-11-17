from app import app
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy configuration with Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Password@4321@localhost/FlaskApiDb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating SQLAlchemy instance
db = SQLAlchemy(app)

