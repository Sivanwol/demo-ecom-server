from src.exceptions.error import Error
from src.utils.common_methods import logger


class UnknownRolesOrNotMatched(Error):
    """Raised when an operation attempts try create owner user but failed
        allowed.

        Attributes:
            email -- user email that try creating into
        """

    def __init__(self, roles_name):
        self.message = 'one of the roles name dose not existed {}'.format(role_name for role_name in roles_name)
        logger.error(self.message)
