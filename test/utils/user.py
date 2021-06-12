from src.utils.enums import RolesTypes


class UserTestUtills:
    def __init__(self, test_object):
        self.test_object = test_object

    def create_platforms_users(self):
        emails = {
            'accounts': [],
            'support': []
        }
        for i in range(6, 15):
            email = self.test_object.fake.email()
            emails['accounts'].append(email)
            self.test_object.create_user(email, [RolesTypes.Accounts.value], True)

        for i in range(2, 5):
            email = self.test_object.fake.email()
            emails['support'].append(email)
            self.test_object.create_user(email, [RolesTypes.Support.value], True)
        print('Total Users {} , Total Account Users {} , Total Support Users {}'.format(
            len(emails['accounts']) + len(emails['support']),
            len(emails['accounts']),
            len(emails['support'])
        ))
        return emails

    def create_3pages_platform_users(self):
        emails = {
            'accounts': [],
            'support': []
        }

        for i in range(2, 5):
            email = self.test_object.fake.email()
            emails['accounts'].append(email)
            self.test_object.create_user(email, [RolesTypes.Accounts.value], True)

        for i in range(58, 66):
            email = self.test_object.fake.email()
            emails['support'].append(email)
            self.test_object.create_user(email, [RolesTypes.Support.value], True)
        print('Total Users {} , Total Account Users {} , Total Support Users {}'.format(
            len(emails['accounts']) + len(emails['support']),
            len(emails['accounts']),
            len(emails['support'])
        ))
        return emails
