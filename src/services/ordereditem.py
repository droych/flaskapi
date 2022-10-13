from flask import jsonify, request
from flask_jwt_extended import jwt_required

from src.db.connections import mysql
from flask_restful import Resource

from src.utils.admindec import admin_required


class Orderitemlist(Resource):
    @jwt_required()
    @admin_required([1])
    def get(self):
        global cursor
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""select * from orderitems""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    def post(self):
        global response, cursor, cur, conn
        try:
            json_data = request.get_json(force=True)
            _order_id = json_data['order_id']
            _user_name = json_data['user_name']
            _product_name = json_data['product_name']
            _user_id = json_data['user_id']
            _product_id = json_data['product_id']
            _order_date = json_data['order_date']
            cursor = mysql.connection.cursor()
            cursor.execute( "INSERT INTO orderitems (order_id , user_id , user_name, product_name, product_id, order_date ) VALUES (%s, %s, %s, %s, %s, %s)",
                (_order_id,_user_id,_user_name,_product_name,_product_id,_order_date))
            mysql.connection.commit()
            response = jsonify('order added!')
            response.status_code = 200
            cursor.close()
            return response
        except Exception as e:
            print(e)



class Orderitem(Resource):
    def get(self, order_id):
        global cursor
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM orderitems WHERE id = %s",  (order_id,))
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    def put(self, id):
        global cursor
        try:
            json_data = request.get_json(force=True)
            _order_date = json_data['order_date']
            _user_id = json_data['user_id']
            _product_id = json_data['product_id']
            _user_name = json_data['user_name']
            _product_name = json_data['product_name']
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE orderitems SET order_date =%s,user_id =%s,product_id =%s, user_name =%s,product_name =%s WHERE order_id =%s",
                ( _order_date, _user_id,_product_id, _user_name, _product_name, id,))
            mysql.connection.commit()
            response = jsonify('order updated!')
            response.status_code = 200
            return response
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    def delete(self, id):
        global response, cursor
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM orderitems WHERE id=%s", (id,))
            mysql.connection.commit()
            response = jsonify('order deleted!')
            response.status_code = 200
            return response
        except Exception as e:
            print(e)
        finally:
            cursor.close()


