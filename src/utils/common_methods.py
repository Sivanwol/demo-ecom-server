from urllib.parse import urlparse
from flask import request, url_for
from validator import validate
from src.exceptions.unable_create_owner_user import CommandUnableCreateOwnerUser
from src.utils.enums import RolesTypes
from src.utils.firebase_utils import check_user, create_firebase_user
from src.utils.responses import response_error


def verify_uid(uid):
    from src.services.user import UserService
    userService = UserService()
    rules = {"uid": "required|min:10"}
    result = validate({"uid": uid}, rules)  # True
    if result:
        return userService.user_exists(uid)
    else:
        return False


def verify_response():
    if not request.is_json:
        return response_error({"msg": "Missing JSON in request"}, None, 400)


def setup_user(email, password, roles):
    from src.services.user import UserService
    userService = UserService()
    user = check_user(email)
    if user is None:
        print("Firebase user creation")
        user = create_firebase_user(email, password)
    if user is None:
        raise CommandUnableCreateOwnerUser(email)
    user_data = user.__dict__['_data']
    print('owner user {} => {}, {}'.format(email, password, user_data))
    uid = user_data['localId']
    userService.sync_firebase_user(uid, roles, email, user_data['displayName'], True)
    print('owner user create {} => {}'.format(email, uid))


def setup_owner_user(email, password):
    from src.services.roles import RolesService
    roleSerivce = RolesService()
    roles = roleSerivce.get_roles([RolesTypes.Owner.value])
    setup_user(email, password, roles)


def setup_accounts_user(email, password):
    from src.services.roles import RolesService
    roleSerivce = RolesService()
    roles = roleSerivce.get_roles([RolesTypes.Accounts.value])
    setup_user(email, password, roles)


def setup_support_user(email, password):
    from src.services.roles import RolesService
    roleSerivce = RolesService()
    roles = roleSerivce.get_roles([RolesTypes.SUPPORT.value])
    setup_user(email, password, roles)


def scan_routes(app):
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urlparse("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)
