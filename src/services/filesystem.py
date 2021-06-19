import pathlib


class FileSystem:
    def file_existed(self, src):
        file = pathlib.Path(src)
        if file.exists():
            return True
        return False
