from flask import jsonify


def generic_response(code, data, message=None, params=None, ws=False):
    if ws:
        return {
            "status": True if code == 200 else False,
            "data": data if code == 200 else {},
            "error_params": params if code != 200 else {},
            "error": message if code != 200 else {}
        }
    return jsonify({
        "status": True if code == 200 else False,
        "data": data if code == 200 else {},
        "error_params": params if code != 200 else {},
        "error": message if code != 200 else {}
    }), code


def response_error(message, params=None, status_code=400, ws=False):
    if params is None:
        params = {}
    return generic_response(status_code, None, message, params, ws)


def response_success(data=None, ws=False):
    if data is None:
        data = {}
    return generic_response(200, data, None, None, ws)


def response_success_paging(items, total, pages, has_next, has_prev, ws=False):
    return response_success({
        "meta": {
            "next": has_next,
            "prev": has_prev,
            "pages": pages,
            "total_items": total,
        },
        "items": items
    }, ws)
