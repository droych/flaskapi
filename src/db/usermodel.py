from src.controller.app import app
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:2176@localhost/flaskapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    user_addreass = db.Column(db.String(80), nullable=False)
    user_email = db.Column(db.String(80), nullable=False)
    def json(self):
        return {'id': self.user_id, 'name': self.user_name,'adress': self.user_addreass, 'email':self.user_email}