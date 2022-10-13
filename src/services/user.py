from flask import jsonify, request
from flask_jwt_extended import jwt_required

from src.db.connections import mysql,app
from flask_restful import Resource

from src.utils.admindec import admin_required


class Userlist(Resource):
    @jwt_required()
    @admin_required([1])
    def get(self):
        global cursor
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""select * from user""")
            rows = cursor.fetchall()
            cursor.close()
            return jsonify(rows)
        except Exception as e:
            print(e)







class User(Resource):
    @jwt_required()
    @admin_required([1])
    def get(self, id,**kwargs):
        global cursor
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM user WHERE usser_id = %s",  (id,))
            rows = cursor.fetchall()
            cursor.close()
            return jsonify(rows)
        except Exception as e:
            print(e)

    @jwt_required()
    @admin_required([1])

    def put(self, id,**kwargs):
        global cursor
        try:
            json_data = request.get_json(force=True)
            _user_id = json_data['id']
            _user_name = json_data['user_name']
            _user_address = json_data['user_address']
            _user_email = json_data['user_email']
            cursor = mysql.connection.cursor()
            sql = "UPDATE user SET user_name=%s, user_address=%s,user_email =%s WHERE user_id=%s"
            data = (_user_name, _user_address,_user_email, id)
            cursor.execute = (sql, data)
            mysql.connection.commit()
            response = jsonify('user updated!')
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
            cursor.execute("DELETE FROM user WHERE user_id=%s", (id,))
            mysql.connection.commit()
            response = jsonify('user deleted!')
            response.status_code = 200
            cursor.close()
            return response
        except Exception as e:
            print(e)




