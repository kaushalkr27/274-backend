from flask import Blueprint, request, jsonify, current_app
from database.get_data import get_user_by_email
import jwt

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login', methods=["POST"])
def api2():
    email = request.json['email']
    password = request.json['password']
    user = get_user_by_email(email)['user']
    if password == user['password']:
        token = jwt.encode({'username': email}, current_app.config['SECRET_KEY'])
        return jsonify({'token': token, 'status': 200}), 200
    else:
        return jsonify({'message': 'Password incorrect!', 'status': 401}), 401


@login_blueprint.route('/protected')
def protected():
    try:
        token = request.headers.get('Authorization')
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        username = payload
        return jsonify({'user': username['username']})
    except:
        return jsonify({'error': 'Invalid token'}), 401
