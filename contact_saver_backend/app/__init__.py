from flask import Flask, request
from flask_cors import CORS
from .routes.health import blp as health_blp
from .routes.contacts import blp as contacts_blp
from flask_smorest import Api

app = Flask(__name__)

# Adjust allowed origin if you know your frontend's base URL, for example:
# frontend_origin = "http://localhost:4200"  # Angular default
# For maximum debugging, CORS "*" for now, but recommend setting specific in production
frontend_origin = "*"  # CHANGE to real origin for better security after debugging

CORS(app, resources={r"/*": {"origins": frontend_origin}}, supports_credentials=True)
print(f"[DEBUG] Flask app initialized - CORS configured for origin: {frontend_origin}")

@app.before_request
def log_every_request():
    print(f"[DEBUG] [REQ] {request.method} {request.path} - Headers: {dict(request.headers)}")

@app.after_request
def debug_after_request(response):
    print(f"[DEBUG] [RESP] {request.method} {request.path} - Status: {response.status} - CORS headers: {response.headers.get('Access-Control-Allow-Origin')}")
    return response

app.config["API_TITLE"] = "Contact Saver Backend"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
api.register_blueprint(health_blp)
api.register_blueprint(contacts_blp)
