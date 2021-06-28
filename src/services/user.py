import firebase_admin
from firebase_admin import auth
from flask import Flask
from sqlalchemy import or_, desc, asc

from config.setup import cache
from config.database import db
from src.models import User, Store
from src.schemas import UserSchema
from src.services import FileSystemService, MediaService
from src.utils.enums import AllowSortByDirection
from src.utils.firebase_utils import create_firebase_user
from src.utils.responses import response_error


class UserService:
    def __init__(self,app: Flask, fileSystemService: FileSystemService, mediaService: MediaService):
        self.logger = app.logger
        self.fileSystemService = fileSystemService
        self.mediaService = mediaService

    user_schema = UserSchema()
    """Verifies the signature and data for the provided JWT.

    Accepts a signed token string, verifies that it is current, was issued
    to this project, and that it was correctly signed by Google.

    Args:
        id_token: A string of the encoded JWT.
        check_revoked: Boolean, If true, checks whether the token has been revoked (optional).

    Returns:
        dict: A dictionary of key-value pairs parsed from the decoded JWT.

    Raises:
        ValueError: If ``id_token`` is a not a string or is empty.
        InvalidIdTokenError: If ``id_token`` is not a valid Firebase ID token.
        ExpiredIdTokenError: If the specified ID token has expired.
        RevokedIdTokenError: If ``check_revoked`` is ``True`` and the ID token has been
            revoked.
        TenantIdMismatchError: If ``id_token`` belongs to a tenant that is different than
            this ``Client`` instance.
        CertificateFetchError: If an error occurs while fetching the public key certificates
            required to verify the ID token.
    """

    def verify_token(self, token, check_revoked=False):
        return auth.verify_id_token(token, check_revoked)

    def get_firebase_user(self, uid):
        return auth.get_user(uid)

    @cache.memoize(50)
    def get_user(self, uid, return_model=False):
        user = User.query.filter_by(uid=uid).first()
        if not return_model:
            return self.user_schema.dump(user, many=False)
        return user

    # todo: need add better filters with the store that include things like store name and more...
    @cache.memoize(50)
    def get_users(self, filters, orders, per_page, page, is_inactive=False, show_store_users=False):
        query = User.query
        query_filters = []
        # setup filter params
        if not filters['platform']:
            if len(filters['stores']) > 0:
                query_filters.append(User.store_code.in_(tuple(filters['stores'])))
        if len(filters['emails']) > 0:
            query_filters.append(User.email.in_(tuple(filters['emails'])))
        if len(filters['names']) > 0:
            for name in filters['names']:
                query_filters.append(User.fullname.ilike('%{}%'.format(name.lower())))
        if len(filters['countries']) > 0:
            query_filters.append(User.country.in_(tuple(filters['countries'])))

        # building the query filter

        # for query_filter in query_filters:
        query = query.filter(or_(*query_filters))
        if not is_inactive:
            query = query.filter_by(is_active=True)
        else:
            query = query.filter_by(is_active=False)

        if filters['platform']:
            if show_store_users:
                query = query.filter(or_(User.store_code.isnot(None), User.store_code == None))
            else:
                query = query.filter_by(store_code=None)

        if len(orders) <= 0:
            query = query.order_by(User.created_at.desc())
        else:
            for order in orders:
                if order['sort'] == AllowSortByDirection.DESC:
                    query = query.order_by(desc(order['field'].value))
                else:
                    query = query.order_by(asc(order['field'].value))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @cache.memoize(50)
    def get_active_user(self, uid, return_model=False):
        user = User.query.filter_by(uid=uid, is_active=True).first()
        if not return_model:
            return self.user_schema.dump(user, many=False)
        return user

    @cache.memoize(50)
    def user_exists(self, uid) -> bool:
        user = User.query.filter_by(uid=uid, is_active=True).first()
        if user is None:
            return False
        return True

    def user_has_any_role_matched(self, uid, roles):
        user = self.get_user(uid, True)
        return user.has_any_role(roles)

    def user_has_role_matched(self, uid, roles) -> bool:
        user = self.get_user(uid, True)
        return user.has_role(roles)

    def check_user_part_store(self, uid, store_code) -> bool:
        store = Store.query.filter_by(store_code=store_code).first()
        user = self.get_user(uid, True)
        if store is None or user is None:
            return False
        if store.owner_user_uid == uid or user.store_code == store_code:
            return True
        return False

    def check_user_auth(self, request, existed_on_system):
        if not request.headers.get('authorization'):
            return response_error('No token provided', None, 400)
        try:
            token = request.headers['authorization'].replace('Bearer ', '')
            firebase_obj = auth.verify_id_token(token)
            if existed_on_system:
                uid = firebase_obj["uid"]
                user_exist = self.user_exists(uid)
                if not user_exist:
                    return response_error('user not active', None, 400)
            return firebase_obj["uid"]
        except:
            return response_error('Invalid token provided', None, 400)

    def check_user_auth_socket(self, token, existed_on_system):
        token = token.replace('Bearer ', '')
        firebase_obj = auth.verify_id_token(token)
        try:
            if existed_on_system:
                uid = firebase_obj["uid"]
                user_exist = self.user_exists(uid)
                if not user_exist:
                    return None
            return firebase_obj["uid"]
        except:
            return None

    def update_user_info(self, uid, user_data):
        user = self.get_user(uid, True)
        user.fullname = user_data.fullname
        user.address1 = user_data.address1
        user.address2 = user_data.address2
        user.country = user_data.country
        user.currency = user_data.currency
        db.session.merge(user)
        db.session.commit()

    def update_user_store_owner(self, uid, store_code):
        user = self.get_user(uid, True)
        user.store_code = store_code
        db.session.merge(user)
        db.session.commit()

    def mark_user_passed_tutorial(self, uid):
        user = self.get_user(uid, True)
        user.is_pass_tutorial = True
        db.session.merge(user)
        db.session.commit()

    def toggle_freeze_user(self, uid):
        user = self.get_user(uid, True)
        user.is_active = not user.is_active
        firebase_admin.auth.update_user(uid, disabled=not user.is_active)
        db.session.merge(user)
        db.session.commit()
        auth.revoke_refresh_tokens(uid)

    ''' Will create staff user for the store (this will not for customer as he work on different workflow'''

    def create_user(self, email, fullname, password, roles, store_code):
        user_obj = create_firebase_user(email, password)
        uid = user_obj.uid
        self.sync_firebase_user(uid, roles, email, fullname, True, store_code, True)
        return self.get_user(uid)

    # TODO: Remove this method
    def query_platform_users(self, filters, per_page, page, include_stores=False):
        users = User.query
        if not include_stores:
            users.filter_by(store_code=None)

        names = filters['names']
        if len(names) > 0:
            users.filter(or_(User.fullname.like('%{}%'.format(v)) for v in names))
        users.order_by(User.store_code.desc(), User.fullname.desc())
        return users.paginate(page, per_page, False)

    # TODO: Remove this method
    def query_store_users(self, store_code, filters, per_page, page):
        users = User.query.filter_by(store_code=store_code)
        names = filters['names']
        if len(names) > 0:
            users.filter(or_(User.fullname.lower().like('%{}%'.format(v.lower()) for v in names)))
        users.order_by(User.fullname.desc())
        return users.paginate(page, per_page, False)

    def check_user_roles(self, uid, *requirements_roles):
        """ Return True if the user has all of the specified roles. Return False otherwise.
            has_roles() accepts a list of requirements:
                has_role(requirement1, requirement2, requirement3).
            Each requirement is either a role_name, or a tuple_of_role_names.
                role_name example:   'manager'
                tuple_of_role_names: ('funny', 'witty', 'hilarious')
            A role_name-requirement is accepted when the user has this role.
            A tuple_of_role_names-requirement is accepted when the user has ONE of these roles.
            has_roles() returns true if ALL of the requirements have been accepted.
            For example:
                has_roles('a', ('b', 'c'), d)
            Translates to:
                User has role 'a' AND (role 'b' OR role 'c') AND role 'd'"""
        user = self.get_user(uid, True)
        role_names = user.roles
        for requirement in requirements_roles:
            if isinstance(requirement, (list, tuple)):
                # this is a tuple_of_role_names requirement
                tuple_of_role_names = requirement
                authorized = False
                for role_object in role_names:
                    if role_object.name in tuple_of_role_names[0]:
                        # tuple_of_role_names requirement was met: break out of loop
                        if role_object.is_active:
                            authorized = True
                            break
                if not authorized:
                    return False  # tuple_of_role_names requirement failed: return False
            else:
                # the user must have this role
                for role_object in role_names:
                    if not role_object.is_active:
                        return False
                    if role_object.name in requirements_roles:
                        return False  # role_name requirement failed: return False

            # All requirements have been met: return True
        return True

    def sync_firebase_user(self, uid, roles, email, fullname, is_platform_user, store_code=None, is_new_user=True):
        self.fileSystemService.create_user_folder_initialize(uid)
        user = User(uid, email, fullname, True, is_new_user)
        if not is_platform_user:
            if store_code is not None:
                user.store_code = store_code
            user.is_pass_tutorial = False
            if not is_new_user:
                user.is_pass_tutorial = True
        user.add_user_roles(roles)
        db.session.add(user)
        db.session.commit()
