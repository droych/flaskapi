from flask import jsonify, request
from flask_jwt_extended import jwt_required

from src.db.connections import mysql
from flask_restful import Resource

from src.utils.admindec import admin_required


#from src.services.auth import jwt_required,admin_required

class Productlist(Resource):
    def get(self):
        global cursor
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""select * from product""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    @jwt_required()
    @admin_required(1)
    def post(self, **kwargs):
        global response, cursor, cur, conn
        try:
            json_data = request.get_json(force=True)
           # _product_id = json_data['product_id']
            _product_name = json_data['product_name']
            _product_rate = json_data['product_rate']
            _quantity = json_data['quantity']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO product (product_name, product_rate, quantity) VALUES ( %s, %s,%s)",
                        ( _product_name, _product_rate,_quantity))
            mysql.connection.commit()
            response = jsonify('product added!')
            response.status_code = 200
            cur.close()
            return response
        except Exception as e:
            print(e)




class Product(Resource):
    def get(self, product_id):
        global cursor
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM product WHERE product_id = %s",  (product_id,))
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
            _product_name = json_data['product_name']
            _product_rate = json_data['product_rate']

            _quantity = json_data['quantity']
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE product SET product_name =%s, product_rate =%s,quantity =%s WHERE product_id =%s",
                           (_product_name, _product_rate,_quantity, id,))
            mysql.connection.commit()
            response = jsonify('product updated!')
            response.status_code = 200
            cursor.close()
            return response
        except Exception as e:
            print(e)

    @jwt_required()
    @admin_required([1])
    def delete(self, id,**kwargs):

        global response, cursor
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM product WHERE product_id=%s", (id,))
            mysql.connection.commit()
            response = jsonify('product deleted!')
            response.status_code = 200
            cursor.close()
            return response
        except Exception as e:
            print(e)




