from flask import Blueprint, request, jsonify, current_app
from database.get_data import get_user_by_email
from database.get_data import get_top_products
from database.get_data import get_reorders, get_pred, get_all_products
import jwt

dashboard_blueprint = Blueprint('dashboard', __name__)


@dashboard_blueprint.route('/api1', methods=["GET"])
def api1():
    try:
        token = request.headers.get('Authorization')
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'Aisles': 134, 'Departments': 21, 'Products': 49688, 'Orders': 3421083})
    except:
        return jsonify({'error': 'Invalid token'}), 401


@dashboard_blueprint.route('/top-products', methods=["GET"])
def api2():
    try:
        token = request.headers.get('Authorization')
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        data = get_top_products()
        return jsonify({'data': data, 'status': 200})
    except:
        return jsonify({'error': 'Invalid token'}), 401


@dashboard_blueprint.route('/reorders', methods=["GET"])
def get_top_reorders():
    token = request.headers.get('Authorization')
    payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    data = get_reorders()
    return jsonify({'data': data, 'status': 200})


@dashboard_blueprint.route('/predict', methods=["GET"])
def get_res():
    token = request.headers.get('Authorization')
    payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    data = get_pred(request.args.get('user_id'), request.args.get('product_id'))
    return jsonify({'data': data, 'status': 200})


@dashboard_blueprint.route('/all-products', methods=["GET"])
def prods():
    token = request.headers.get('Authorization')
    payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    data = get_all_products()
    return jsonify({'data': data, 'status': 200})

