import json
from flask import jsonify
from google.cloud import bigquery
from google.cloud.bigquery.schema import SchemaField

job_config = bigquery.QueryJobConfig(use_legacy_sql=True)
CREDS = './database/cmpe-274-381208-51e241a4a657.json'
client = bigquery.Client.from_service_account_json(json_credentials_path=CREDS)

USER_SCHEMA = [SchemaField(name="email", field_type="STRING", mode="REQUIRED"),
               SchemaField(name="password", field_type="STRING", mode="REQUIRED"),
               SchemaField(name="full_name", field_type="STRING", mode="REQUIRED")]


def check_if_user_exists(email):
    query = f"SELECT email FROM instacart.users WHERE email='{email}'"
    query_job = client.query(query)
    results = query_job.result().to_dataframe()['email'].tolist()
    if results:
        return True
    else:
        return False


def get_user_by_email(email):
    query = f"SELECT * FROM instacart.users WHERE email='{email}'"
    query_job = client.query(query)
    results = query_job.to_dataframe().to_dict(orient='records')[0]
    user = {
        'email': results['email'],
        'password': results['password'],
        'full_name': results['full_name']
    }
    if user:
        return {'user': user, 'message': 'User found', 'status': 200}
    else:
        return {'message': 'User not found', 'status': 404}


def insert_user(email, password, full_name):
    user_exists_check = check_if_user_exists(email)
    if not user_exists_check:
        row_to_insert = [{'email': str(email), 'password': str(password), 'full_name': str(full_name)}]
        errors = client.insert_rows('instacart.users', row_to_insert, selected_fields=USER_SCHEMA)
        if not errors:
            return {'message': 'User added successfully', 'status': 200}
        else:
            return {'message': 'Could not add user', 'errors': errors, 'status': 400}
    else:
        return {'message': 'User already exists', 'status': 409}


def get_top_products():
    query = """
        SELECT op.product_id, COUNT(*) AS count, p.product_name
        FROM instacart.order_products__prior op
        JOIN instacart.products p
        ON op.product_id = p.product_id
        GROUP BY op.product_id, p.product_name
        ORDER BY count DESC
        LIMIT 10
        """
    rows = client.query(query).result()
    results = [dict(row) for row in rows]
    return results


def get_reorders():
    query = """
        SELECT p.product_name, COUNTIF(o.reordered = 1) / COUNT(*) AS proportion_reordered
        FROM `cmpe-274-381208.instacart.order_products__prior` o
        LEFT JOIN `cmpe-274-381208.instacart.products` p
        ON o.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY proportion_reordered DESC
        LIMIT 10
        """
    rows = client.query(query).result()
    results = [dict(row) for row in rows]
    return results


def get_pred(user_id, product_id):
    query = """
    SELECT * 
    FROM `cmpe-274-381208.instacart.pred` 
    WHERE user_id = {} AND product_id = {}
    """.format(user_id, product_id)
    rows = client.query(query).result()
    results = [dict(row) for row in rows]
    return results


def get_all_products():
    query = """SELECT product_name, product_id FROM `cmpe-274-381208.instacart.products` LIMIT 50"""
    rows = client.query(query).result()
    results = [dict(row) for row in rows]
    return results


def get_order_by_hours():
    query = """SELECT order_hour_of_day, COUNT(*) as count
    FROM `cmpe-274-381208.instacart.orders`
    GROUP BY order_hour_of_day
    ORDER BY order_hour_of_day"""
    rows = client.query(query).result()
    results = [dict(row) for row in rows]
    return results


def get_orders_by_day_of_the_week():
    query = """SELECT order_dow, COUNT(*) as count
    FROM `cmpe-274-381208.instacart.orders`
    GROUP BY order_dow
    ORDER BY order_dow"""
    rows = client.query(query).result()
    results = [dict(row) for row in rows]
    return results



