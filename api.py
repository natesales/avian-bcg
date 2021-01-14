import json
from functools import wraps

import requests
from bson import ObjectId
from flask import Flask, request, Response
from pymongo import MongoClient

app = Flask(__name__)
db = MongoClient("mongodb://localhost:27017")["avian"]

config = {
    "network": {
        "asn": 34553,
        "name": "Packetframe"
    },
    "routers": ["core1.pdx1", "core1.fmt1"]
}


class JSONResponseEncoder(json.JSONEncoder):
    """
    BSON ObjectId-safe JSON response encoder
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def _resp(success: bool, message: str, data: object = None):
    """
    Return a JSON API response
    :param success: did the request succeed?
    :param message: what happened?
    :param data: any application specific data
    :return:
    """

    return Response(JSONResponseEncoder().encode({
        "meta": {
            "success": success,
            "message": message
        },
        "data": data
    }), mimetype="application/json")


def with_json(*outer_args):
    """
    Get JSON API request body
    :param outer_args: *args (str) of JSON keys
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _json_body = {}
            for arg in outer_args:
                if not request.json:
                    return _resp(False, "JSON body must not be empty")
                val = request.json.get(arg)
                if val is not None:
                    _json_body[arg] = val
                else:
                    return _resp(False, "Required argument " + arg + " is not defined.")
            return func(*args, **kwargs, json_body=_json_body)

        return wrapper

    return decorator


@app.route("/config", methods=["GET"])
def get_config():
    return _resp(True, "Retrieved config", config)


@app.route("/peeringdb/info", methods=["POST"])
@with_json("asn")
def peeringdb_info(json_body):
    """
    Get network info from PeeringDB
    :return:
    """

    pdb_resp = requests.get(f"https://peeringdb.com/api/net?asn={json_body['asn']}")
    if pdb_resp.status_code != 200 or not pdb_resp.json()["data"]:
        return _resp(False, "PeeringDB page not found")

    return _resp(True, "Retrieved data from PeeringDB", data=pdb_resp.json()["data"])


@app.route("/sessions", methods=["PUT"])
@with_json("asn", "description", "profile", "validateRpki", "validateIrr", "validateMaxPfx", "asSet", "maxPfx4", "maxPfx6", "router")
def sessions_put(json_body):
    """
    Register a BGP session in the database
    :return:
    """

    db["sessions"].insert_one(json_body)

    return _resp(True, "Added session")


@app.route("/sessions", methods=["GET"])
def sessions_get():
    return _resp(True, "Retrieved sessions", list(db["sessions"].find()))


app.run()
