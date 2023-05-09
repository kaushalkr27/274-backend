from flask import Flask
from apis.login import login_blueprint
from apis.signup import signup_blueprint
from apis.dashboard import dashboard_blueprint
from flask_cors import CORS

application = app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'some-secret-key'


@app.route('/')
def hello_world():
    return 'Hello, World!'


app.register_blueprint(login_blueprint)
app.register_blueprint(signup_blueprint)
app.register_blueprint(dashboard_blueprint)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
