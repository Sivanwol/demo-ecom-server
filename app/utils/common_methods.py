from flask import request
from validator import validate

from app.utils.responses import response_error


def verify_uid(uid):
    rules = {"uid": "require|min:10"}
    result = validate({uid: uid}, rules)
    if result:
        return True
    else:
        return False


def verify_response():
    if not request.is_json:
        return response_error({"msg": "Missing JSON in request"}, None, 400)
