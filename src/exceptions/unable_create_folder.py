from src.exceptions.error import Error


class UnableCreateFolder(Error):
    """Raised when an operation attempts try create owner user but failed
        allowed.

        Attributes:
            email -- user email that try creating into
        """

    def __init__(self, folder_name, sub_path=None):
        if sub_path is None:
            sub_path = ''
        self.message = 'unable create folder code %s on sub_path (%s)' % (folder_name, sub_path)
