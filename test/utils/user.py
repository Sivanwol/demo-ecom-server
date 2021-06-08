from src.utils.enums import RolesTypes


class UserTestUtills:
    def __init__(self, test_object):
        self.test_object = test_object

    def create_platforms_users(self):
        self.create_user(self.test_object.fake.email(), [RolesTypes.Accounts.value], True)
        self.create_user(self.test_object.fake.email(), [RolesTypes.Accounts.value], True)
        self.create_user(self.test_object.fake.email(), [RolesTypes.Accounts.value], True)
        self.create_user(self.test_object.fake.email(), [RolesTypes.Accounts.value], True)
        self.create_user(self.test_object.fake.email(), [RolesTypes.Support.value], True)
        self.create_user(self.test_object.fake.email(), [RolesTypes.Support.value], True)
        self.create_user(self.test_object.fake.email(), [RolesTypes.Support.value], True)
        self.create_user(self.test_object.fake.email(), [RolesTypes.Reports.value], True)

    def create_3pages_platform_users(self):
        self.create_user(self.test_object.fake.email(), [RolesTypes.Accounts.value], True)
        self.create_user(self.test_object.fake.email(), [RolesTypes.Reports.value], True)
        for i in range(50,60):
            self.create_user(self.test_object.fake.email(), [RolesTypes.Support.value], True)