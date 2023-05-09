from flask import Blueprint, request, jsonify
from database.get_data import insert_user

signup_blueprint = Blueprint('sign_up', __name__)


@signup_blueprint.route('/signup', methods=["POST"])
def signup():
    email = request.json['email']
    password = request.json['password']
    full_name = request.json['full_name']
    inserted = insert_user(email, password, full_name)
    return jsonify({'message': inserted['message'], 'status': inserted['status']}), inserted['status']
