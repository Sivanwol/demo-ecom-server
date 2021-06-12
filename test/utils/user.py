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
            name = self.test_object.fake.name()
            email = self.test_object.fake.email()
            user_info = {
                'email': email,
                'name': name
            }
            emails['accounts'].append(user_info)
            self.test_object.create_user(email, name, [RolesTypes.Accounts.value], True)

        for i in range(2, 5):
            name = self.test_object.fake.name()
            email = self.test_object.fake.email()
            user_info = {
                'email': email,
                'name': name
            }
            emails['support'].append(user_info)
            self.test_object.create_user(email, name, [RolesTypes.Support.value], True)
        print('Total Users {} , Total Account Users {} , Total Support Users {}'.format(
            len(emails['accounts']) + len(emails['support']),
            len(emails['accounts']),
            len(emails['support'])
        ))
        return emails

    def create_inactive_platform_users(self):
        emails = self.create_platforms_users()
        for i in range(2, 5):
            name = self.test_object.fake.name()
            email = self.test_object.fake.email()
            user_info = {
                'email': email,
                'name': name
            }
            emails['support'].append(user_info)
            self.test_object.create_user(email, name, [RolesTypes.Support.value], True, None, None, False)

    def create_3pages_platform_users(self):
        emails = {
            'accounts': [],
            'support': []
        }

        for i in range(2, 5):
            name = self.test_object.fake.name()
            email = self.test_object.fake.email()
            user_info = {
                'email': email,
                'name': name
            }
            emails['accounts'].append(user_info)
            self.test_object.create_user(email, name, [RolesTypes.Accounts.value], True)

        for i in range(58, 66):
            name = self.test_object.fake.name()
            email = self.test_object.fake.email()
            user_info = {
                'email': email,
                'name': name
            }
            emails['support'].append(user_info)
            self.test_object.create_user(email, name, [RolesTypes.Support.value], True)
        print('Total Users {} , Total Account Users {} , Total Support Users {}'.format(
            len(emails['accounts']) + len(emails['support']),
            len(emails['accounts']),
            len(emails['support'])
        ))
        return emails
