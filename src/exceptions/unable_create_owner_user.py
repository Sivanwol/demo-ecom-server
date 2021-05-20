from src.exceptions.error import Error


class CommandUnableCreateOwnerUser(Error):
    """Raised when an operation attempts try create owner user but failed
        allowed.

        Attributes:
            email -- user email that try creating into
        """

    def __init__(self, email):
        self.message = 'failed create owner user under this email: {} please check firebase console'.format(email)
