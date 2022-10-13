import functools

from flask import jsonify

from flask_jwt_extended import get_jwt_identity,jwt_required
from src.db.connections import mysql


def user_required(role_authorized):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            cursor = mysql.connection.cursor()
            cursor.execute('select user_name from users where user_name =%s', (current_user,))
            users = cursor.fetchone()
            print(users)
            if users is None:
                return jsonify(
                    {'status': 400, 'message': 'Authentication failure : please register fisrt or check username ',
                     'username': current_user})
            else:
                user = users[0]
                print(user)
                if current_user in users:
                    cursor.callproc('storeuserlogin', (current_user,))
                    data = cursor.fetchall()
                    print(data)
                    if data:
                        data = data[0][0]
                        if data in role_authorized:
                               kwargs["logged_user"] = current_user
                               return fn(*args, **kwargs)
                        else:
                                  return {'message': 'You are not authorized to access this data.'}, 403

        return wrapper

    return decorator