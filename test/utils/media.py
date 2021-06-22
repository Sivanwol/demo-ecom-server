from uuid import uuid4

from config.database import db
from src.models import MediaFolder


class MediaTestUtills:
    def __init__(self, test_object):
        self.test_object = test_object

    def create_media_folder_parents(self, uid):
        list_of_folders = []
        root_code = str(uuid4())
        db.session.add(MediaFolder(root_code, uid, "root-1", 'root-1', None, True, 1, None))
        for i in range(3):
            chile_lvl1_code = str(uuid4())
            db.session.add(MediaFolder(chile_lvl1_code, uid, "root-1-child-1-lvl-1", 'root-1-child-1-lvl-1', None, True, 2, root_code))
            for r in range(3):
                chile_lvl2_code = str(uuid4())
                db.session.add(MediaFolder(chile_lvl2_code, uid, "root-1-child-1-lvl-2", 'root-1-child-1-lvl-2', None, True, 3, chile_lvl1_code))
        root_code = str(uuid4())
        list_of_folders.append(root_code)
        db.session.add(MediaFolder(root_code, uid, "root-2", 'root-2', None, True, 1, None))
        for i in range(3):
            chile_lvl1_code = str(uuid4())
            list_of_folders.append(chile_lvl1_code)
            db.session.add(MediaFolder(chile_lvl1_code, uid, "root-2-child-2-lvl-1", 'root-2-child-2-lvl-1', None, True, 2, root_code))
            for r in range(3):
                chile_lvl2_code = str(uuid4())
                list_of_folders.append(chile_lvl2_code)
                db.session.add(MediaFolder(chile_lvl2_code, uid, "root-2-child-2-lvl-2", 'root-2-child-2-lvl-2', None, True, 3, chile_lvl1_code))
        db.session.commit()
        return list_of_folders
