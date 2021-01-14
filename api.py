import ipaddress
import json
from functools import wraps

from bson import ObjectId
from flask import Flask, request, Response
from pymongo import MongoClient

from rendering import frr

app = Flask(__name__)
db = MongoClient("mongodb://localhost:27017")["avian"]


config = {
    "network": {
        "asn": 34553,
        "name": "Packetframe"
    },
    "routers": {
        "core1.pdx1": {
            "platform": "frr",
            "origin4": ["192.0.2.0/24"],
            "origin6": ["2001:db8::/48"]
        },
        "core1.fmt1": {
            "platform": "frr"
        },
        "core1.dfw1": {
            "platform": "frr",
            "origin4": ["192.0.2.0/24", "192.0.3.0/24"],
            "origin6": ["2001:db8::/48", "2001:db8:3::/48"]
        },
    }
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


@app.route("/sessions", methods=["PUT"])
@with_json("asn", "description", "profile", "validateRpki", "validateIrr", "validateMaxPfx", "asSet", "maxPfx4", "maxPfx6", "router", "neighborAddress")
def sessions_put(json_body):
    """
    Register a BGP session in the database
    :return:
    """

    try:
        ipaddress.ip_address(json_body["neighborAddress"])
    except ValueError:
        return _resp(False, "Invalid neighbor address")

    db["sessions"].insert_one(json_body)

    return _resp(True, "Added session")


@app.route("/sessions", methods=["GET"])
def sessions_get():
    return _resp(True, "Retrieved sessions", list(db["sessions"].aggregate([{"$addFields": {"id": "$_id"}}])))


@app.route("/render/<router>", methods=["GET"])
def render(router):
    if router not in config["routers"]:
        return _resp(False, f"router {router} doesn't exist")

    if config["routers"][router]["platform"] == "frr":
        renderer = frr
    else:
        return _resp(False, "router platform doesn't have a renderer")

    return _resp(True, "render complete", renderer.render(config=config, router=router, sessions=list(db["sessions"].find({"router": router}))))


app.run(debug=True)
