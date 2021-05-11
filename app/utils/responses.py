from flask import jsonify


def generic_response(code, data, message=None, params=None):
    return jsonify({
        "status": True if code == 200 else False,
        "data": data if code == 200 else None,
        "error_params": params if code != 200 else None,
        "error": message if code != 200 else None
    }), code


def response_error(message, params=None):
    if params is None:
        params = {}
    return generic_response(500, None, message, params)


def response_success(data=None):
    if data is None:
        data = {}
    return generic_response(200, data)
