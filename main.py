from src.services.auth import Registration,login,Logout,Refresh,Admin,User
from src.common.common import api,app
from src.services.order import Orderlist,Order
from src.services.user import Userlist
from src.services.ordereditem import Orderitemlist,Orderitem
from src.services.product import Productlist,Product


api.add_resource(Orderitemlist, '/orderitems', endpoint='Orderitems')
api.add_resource(Orderitem, '/orderitem/<int:id>', endpoint='Orderitem')
api.add_resource(Orderlist, '/orders', endpoint='orders')
api.add_resource(Order, '/order/<int:id>', endpoint='order')
api.add_resource(Productlist, '/products', endpoint='products')
api.add_resource(Product, '/product/<int:id>', endpoint='product')
api.add_resource(Userlist, '/users', endpoint='users')
api.add_resource(User, '/user/<int:id>', endpoint='user')
api.add_resource(Registration,'/register', endpoint='register')
api.add_resource(login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Refresh, '/refresh', endpoint='refresh')
api.add_resource(Admin, '/admin', endpoint='admin')
if __name__ == "__main__":
    app.run(debug=True, port=8900)
