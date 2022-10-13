from src.controller.app import app
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:2176@localhost/flaskapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Ordereditems(db.Model):
    __tablename__ = 'ordereditem'
    order_id = db.Column(db.Integer, primary_key=True,foregin_key=True)
    user_name = db.Column(db.String(80),foregin_key=True, nullable=False)
    product_name = db.Column(db.String(80),foregin_key=True, nullable=False)
    User_id = db.Column(db.Integer,foregin_key=True)
    order_date = db.Column(db.date, nullable=False)
    item_rate = db.db.Column(db.Double, nullable=False)