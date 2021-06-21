from src.exceptions.error import Error


class SettingsNotSync(Error):
    """Raised when an operation attempts try create owner user but failed
        allowed.

        Attributes:
            email -- user email that try creating into
        """

    def __init__(self):
        self.message = 'Setting workflow not sync with redis please sync'
