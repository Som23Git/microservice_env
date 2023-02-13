import os
import sqlite3
import redis
from dotenv import load_dotenv
from flask import Flask, request
from elasticapm.contrib.flask import ElasticAPM

# import sqlite3
# from flask import Flask, request
# initialize using environment variables
# from elasticapm.contrib.flask import ElasticAPM
# # app = Flask(__name__)
# apm = ElasticAPM(app)
app = Flask(__name__)
load_dotenv('.env')

# or configure to use ELASTIC_APM in your application's settings
app.config['ELASTIC_APM'] = {
# Set the required service name. Allowed characters:
# a-z, A-Z, 0-9, -, _, and space
'SERVICE_NAME': 'Redis Sqlite and Python Flask Microservice',

# Use if APM Server requires a secret token
'SECRET_TOKEN': os.environ.get("SECRET_TOKEN"),

# Set the custom APM Server URL (default: http://localhost:8200)
'SERVER_URL': os.environ.get("SERVER_URL"),

# Set the service environment
'ENVIRONMENT': 'production',

'DEBUG': 'DEBUG'
}

apm = ElasticAPM(app)

# app = Flask(__name__)

redis_conn = redis.Redis(host="localhost", port=6379, db=0)

@app.route("/log", methods=["POST"])
def log():
    message = request.form["message"]

    # Store the message in SQLite
    sqlite_conn = sqlite3.connect("logs.db")
    cursor = sqlite_conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS logs (message text)")
    cursor.execute("INSERT INTO logs (message) values (?)", (message,))
    sqlite_conn.commit()
    sqlite_conn.close()

    # Store the message in Redis
    redis_conn.rpush("logs", message)

    return "Logged: {}".format(message)

if __name__ == "__main__":
    app.run(debug=True)
