import os
import sqlite3
from flask import Flask, request
from dotenv import load_dotenv
# initialize using environment variables
# from elasticapm.contrib.flask import ElasticAPM
# # app = Flask(__name__)
# apm = ElasticAPM(app)
app = Flask(__name__)
load_dotenv('.env')

# or configure to use ELASTIC_APM in your application's settings
from elasticapm.contrib.flask import ElasticAPM
app.config['ELASTIC_APM'] = {
# Set the required service name. Allowed characters:
# a-z, A-Z, 0-9, -, _, and space
'SERVICE_NAME': 'SQLite and Python Flask Microservice',

# Use if APM Server requires a secret token
'SECRET_TOKEN': os.environ.get('SECRET_TOKEN'),

# Set the custom APM Server URL (default: http://localhost:8200)
'SERVER_URL': os.environ.get('SERVER_URL'),

# Set the service environment
'ENVIRONMENT': 'production',

'DEBUG': 'DEBUG'
}

apm = ElasticAPM(app)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/log", methods=["POST"])
def log():
    message = request.form["message"]

    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS logs (message text)")
    cursor.execute("INSERT INTO logs (message) values (?)", (message,))
    conn.commit()
    conn.close()

    return "Logged: {}".format(message)

if __name__ == "__main__":
    app.run(debug=True, port=5001)

# cURL command
# curl -X POST -d "message=test message" http://localhost:5000/log
