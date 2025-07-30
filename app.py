import signal
import sys
import json
import requests
from client = storage.Client()
        bucket = client.bucket("fpl-data-bucket-anjali")
        blob = bucket.blob("fpl_data.json")
        blob.upload_from_string(data=json.dumps(data), content_type="application/json")

        return "Data uploaded to Cloud Storage", 200

    except Exception as e:
        return f"Error: {str(e)}", 500

def shutdown_handler(signal_int: int, frame: FrameType) -> None:
    logger.info(f"Caught Signal {signal.strsignal(signal_int)}")
    flush()
    sys.exit(0)

if __name__ == "__main__":
    # Running application locally, outside of a Google Cloud Environment
    signal.signal(signal.SIGINT, shutdown_handler)
    app.run(host="localhost", port=8080, debug=True)
else:
    # handles Cloud Run container termination
    signal.signal(signal.SIGTERM, shutdown_handler)
from types import FrameType
from flask import Flask, request
from google.cloud import storage
from utils.logging import logger, flush

app = Flask(__name__)

@app.route("/", methods=["GET"])
def fetch_and_store():
    logger.info(logField="custom-entry", arbitraryField="custom-entry")
    logger.info("Child logger with trace Id.")

    try:
        url = "https://fantasy.premierleague.com/api/bootstrap-static/"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Remove empty 'scoring' and 'rules' fields under 'events.overrides'
        for event in data.get("events", []):
            overrides = event.get("overrides")
            if isinstance(overrides, dict):
                for key in ["scoring", "rules"]:
                    if key in overrides and (overrides[key] is None or overrides[key] == {}):
                        del overrides[key]

       
