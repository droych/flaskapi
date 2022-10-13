from src.db.connections import mysql
from src.utils.bcrypt import encrypt_password,compare_passwords
from src.utils.jwtconf import generate_login_token,unset_login,refresh

from flask import jsonify, request
from flask_restful import Resource
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, \
    jwt_required

from src.utils.admindec import admin_required



class Registration(Resource):
    def post(self):
        try:
            cursor = mysql.connection.cursor()
            json_data = request.get_json(force=True)
            _user_name = json_data['user_name']
            _fisrt_name = json_data['first_name']
            _last__name = json_data['last_name']
            _email_id = json_data['email_id']
            _user_address = json_data['user_address']
            _mob = json_data['mob']
            _password = json_data['password']
            _hashed = encrypt_password(_password)
            print(_hashed)
            cursor.callproc('regnewusers', (_user_name, _fisrt_name, _last__name, _email_id, _user_address, _mob, _hashed,0))
            data = cursor.fetchall()
            print(data)
            if len(data) == 0:
                mysql.connection.commit()
                response = jsonify(' new user added!')
                response.status_code = 200
                cursor.close()
                return response
            else:
                return {'StatusCode': '300', 'Message': str(data[0])}

        except Exception as e:

            return {'error': str(e)}


class login(Resource):
    def post(self):
        try:
            json_data = request.get_json()
            _user_name = json_data['user_name']
            _password = json_data['password']
            _password = _password.encode('utf-8')
            cursor = mysql.connection.cursor()
            cursor.execute('select user_name from user where user_name =%s', (_user_name,))
            users = cursor.fetchone()
            print(users)
            if users is None:
                return jsonify(
                    {'status': 400, 'message': 'Authentication failure : please register fisrt or check username ',
                     'username': _user_name})
            else:
                user = users[0]
                print(user)
                if _user_name in users:
                    cursor.callproc('userlog', (_user_name,))
                    data = cursor.fetchall()
                    print(data)
                    if data:
                        data = data[0][0]
                        print(data)
                        if compare_passwords(_password, data):
                            return generate_login_token(_user_name), HTTPStatus.OK
                        else:
                            return {'status': 100, 'message': 'Authentication failure: wrong password'}
        except Exception as e:
            return {'error': str(e)}


class Logout(Resource):
    def post(self):
       return unset_login(), HTTPStatus.OK


class Refresh(Resource):
    @jwt_required(optional=True)
    def get(self):
        return refresh(), HTTPStatus.OK


class User(Resource):
    @jwt_required()
    @admin_required([1])
    def get(self, id):
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
    def put(self, id):
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

    def delete(self, user_id):
        global response, cursor
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM user WHERE id=%s", (user_id,))
            mysql.connection.commit()
            response = jsonify('user deleted!')
            response.status_code = 200
            cursor.close()
            return response
        except Exception as e:
            print(e)


class Admin(Resource):
    @jwt_required()
    @admin_required([1])
    def post(self,**kwargs):
        try:
            cursor = mysql.connection.cursor()
            current_user = get_jwt_identity()
            # user = User.query.filter_by(login=name).first_or_404(description="User not found")
            cursor.execute('select user_name from user where user_name =%s', (current_user,))
            y = cursor.fetchall()
            y = y[0][0]
            print(y)
            return y
        except Exception as e:
            return {'error': str(e)}

