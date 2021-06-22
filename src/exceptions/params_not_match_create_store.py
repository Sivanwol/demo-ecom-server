from src.exceptions.error import Error


class ParamsNotMatchCreateStore(Error):
    """Raised when an operation attempts try create owner user but failed
        allowed.

        Attributes:
            email -- user email that try creating into
        """

    def __init__(self, name , owner_user_id , currency_code , description):
        self.message = 'failed create store one of the params not match params: [{},{},{},{}]'.format(name , owner_user_id , currency_code , description)
