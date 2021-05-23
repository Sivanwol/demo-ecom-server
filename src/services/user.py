from firebase_admin import auth

from config.database import db
from src.models import Users
from src.schemas.user_schema import UserSchema
from src.utils.responses import response_error
from src.utils.singleton import singleton


@singleton
class UserService:
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

    def get_user(self, uid):
        user = Users.query.filter_by(uid=uid).first()
        return self.user_schema.dump(user, many=False).data

    def check_user_auth(self, request):
        if not request.headers.get('authorization'):
            return response_error('No token provided', None, 400)
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.uid = user["uid"]
        except:
            return response_error('Invalid token provided', None, 400)

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
        user = self.get_user(uid)
        role_names = user['roles']
        for requirement in requirements_roles:
            if isinstance(requirement, (list, tuple)):
                # this is a tuple_of_role_names requirement
                tuple_of_role_names = requirement
                authorized = False
                for role_object in role_names:
                    if role_object['name'] in tuple_of_role_names[0]:
                        # tuple_of_role_names requirement was met: break out of loop
                        authorized = True
                        break
                if not authorized:
                    return False  # tuple_of_role_names requirement failed: return False
            else:
                # the user must have this role
                for role_object in role_names:
                    if role_object['name'] in requirements_roles:
                        return False  # role_name requirement failed: return False

            # All requirements have been met: return True
        return True

    def sync_user(self, uid, roles):
        user = Users(uid, True)
        user.roles = roles
        db.session.add(user)
        db.session.commit()
