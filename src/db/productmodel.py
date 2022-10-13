
from src.controller.app import app
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:2176@localhost/flaskapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Products(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), nullable=False)
    product_price = db.Column(db.Integer, nullable=False)

    def json(self):
        return {'id': self.product_id, 'name': self.product_name,'rate': self.product_price }

