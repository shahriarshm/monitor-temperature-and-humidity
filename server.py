import os
from flask import Flask, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

app = Flask(__name__)

token = os.environ.get("DB_TOKEN")
org = os.environ.get("DB_ORG")
url = os.environ.get("DB_URL")
bucket = os.environ.get("DB_BUCKET")

write_client = InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)


@app.route("/sensors_data", methods=["POST"])
def sensors_data():
    data = request.get_json()  # example: {'temperature': 28, 'humidity': 24}

    # Store the data in InfluxDB
    point = (
        Point("measurement1")
        .tag("tagname1", "tagvalue1")
        .field("temperature", data["temperature"])
        .field("humidity", data["humidity"])
    )
    write_api.write(bucket=bucket, org="shahriarco", record=point)

    return {"ok": True}

if __name__ == '__main__':
    app.run("0.0.0.0", 8000, True)
