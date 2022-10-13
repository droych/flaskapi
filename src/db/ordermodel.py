from src.controller.app import app
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:2176@localhost/flaskapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Orders(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), nullable=False, foregin_key = True)
    user_name = db.Column(db.String(80), nullable=False, foregin_key = True)
    order_date = db.Column(db.date, nullable=False)
    def json(self):
        return {'id': self.order_id, 'product name': self.product_name,'username': self.user_name, 'order date': self.order_date}