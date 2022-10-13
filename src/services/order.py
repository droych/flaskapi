from flask import jsonify, request
from flask_jwt_extended import jwt_required

from src.db.connections import mysql
from flask_restful import Resource

from src.utils.admindec import admin_required
from src.utils.userdec import user_required


class Orderlist(Resource):
    @jwt_required()
    @user_required([0])
    @admin_required([1])
    def get(self,**kwargs):
        global cursor
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""select * from orders""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    @jwt_required()
    @user_required([0])
    def post(self,**kwargs):
        global response, cursor, cur, conn
        try:
            json_data = request.get_json(force=True)
            _order_id = json_data['order_id']
            _products = json_data['product']
            _user_name = json_data['user_name']
            _user_id = json_data['user_id']

            _order_date = json_data['order_date']

            _user_address = json_data['user_address']
            print(_products)
            cursor = mysql.connection.cursor()
            _cart_total = 0
            purchased = {}
            #resp_data ={}
            for _product in _products:
                # print(_product['product_id'])
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT quantity FROM product where product_id =%s", (_product['product_id'],))
                product_count = cursor.fetchall()
                cursor.execute("SELECT product_rate FROM product where product_id =%s", (_product['product_id'],))
                product_rate = cursor.fetchall()
                cursor.execute("SELECT product_name FROM product where product_id =%s", (_product['product_id'],))
                product_name = cursor.fetchall()
                if product_count:
                    product_count = product_count[0][0]
                    product_rate = product_rate[0][0]
                    product_name = product_name[0][0]
                    print(_product['product_id'], product_count, product_rate)
                    if product_count < int(_product['quantity']):
                        response = jsonify("Sufficient product Count does not exist")
                        return response
                    else:
                        _cart_total += product_rate
                        purchased.update(
                            {"product": {product_name: _product['product_id']}, "quantity": _product['quantity']})

                    cursor.execute("Update  product set quantity=%s where product_id =%s",
                                   (product_count - _product['quantity'], _product['product_id'],))
                    cursor.execute(
                        "INSERT INTO orderitems (order_id ,  product_id, 'quantity' ) VALUES ( %s, %s, %s)",
                        (_order_id, _product['product_id'], _product['quantity']))
                    mysql.connection.commit()
            response = jsonify('order added!', {"cart total": _cart_total, "purchased products": purchased})
            response.status_code = 200

            cursor.close()
            return response

        except Exception as e:
              print(e)

class Order(Resource):
    @jwt_required()
    @user_required([0])
    @admin_required([1])
    def get(self, id,**kwargs):
        global cursor
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM orders WHERE order_id = %s",  (id,))
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    @jwt_required()
    @admin_required([1])
    def put(self, id,**kwargs):

        global cursor
        try:
            json_data = request.get_json(force=True)
            _user_name = json_data['user_name']
            _order_date = json_data['order_date']
            _user_id = json_data['user_id']
            _product_name = json_data['product_name']
            _product_id = json_data['product_id']
            _user_address = json_data['user_address']
            _quantity = json_data['quantity']
            cursor = mysql.connection.cursor()

            cursor.execute("UPDATE orders SET user_name =%s,order_date =%s,user_id =%s,product_name =%s,product_id =%s, user_address =%s,quantity =%s WHERE id =%s",
           (_user_name, _order_date, _user_id, _product_name, _product_id, _user_address, _quantity, id,))
            mysql.connection.commit()
            response = jsonify('order updated!')
            response.status_code = 200
            return response
        except Exception as e:
            print(e)
        finally:
            cursor.close()
    @jwt_required()
    @admin_required([1])
    def delete(self, id,**kwargs):
        global response, cursor
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM orders WHERE order_id=%s", (id,))
            mysql.connection.commit()
            response = jsonify('order deleted!')
            response.status_code = 200
            return response
        except Exception as e:
            print(e)
        finally:
            cursor.close()


