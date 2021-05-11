from validator import validate


def verify_uid(uid):
    rules = {"uid": "require|min:10"}
    result = validate({uid: uid}, rules)
    if result:
        return True
    else:
        return False