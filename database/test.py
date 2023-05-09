# from google.cloud import bigquery
#
# query = """SELECT * FROM instacart.order_products__prior LIMIT 20"""
# job_config = bigquery.QueryJobConfig(use_legacy_sql=True)
#
#
# CREDS = 'cmpe-274-381208-51e241a4a657.json'
# client = bigquery.Client.from_service_account_json(json_credentials_path=CREDS)
# job = client.query(query, job_config=job_config)
# for row in job.result():
#     print(row)
#
# def insert_user():
#
# # def get_user(email):