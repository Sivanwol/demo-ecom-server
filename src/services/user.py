from firebase_admin import auth

from config.database import db
from src.models import Users
from src.utils.singleton import singleton


@singleton
class UserService:
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
        return Users.query.filter_by(uid=uid).first()

    def check_user_roles(self, uid, roles_name):
        user = self.get_user(uid)
        result = False
        for role in user.roles:
            role_name = role.name
            try:
                idx = roles_name.index(role_name)
            except ValueError:
                return False
        return True

    def sync_user(self, uid, roles):
        user = Users(uid, True)
        user.roles = roles
        db.session.add(user)
        db.session.commit()
