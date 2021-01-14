import json
from functools import wraps

import requests
from bson import ObjectId
from flask import Flask, request, Response

app = Flask(__name__)


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


app.run()
