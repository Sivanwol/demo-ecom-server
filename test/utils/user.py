from src.utils.enums import RolesTypes


class UserTestUtills:
    def __init__(self, test_object):
        self.test_object = test_object

    def create_platforms_users(self):
        emails = {
            'accounts': [],
            'support': [],
            'stores': []
        }
        for i in range(6, 15):
            name = self.test_object.fake.name()
            email = self.test_object.fake.email()
            user_info = {
                'email': email,
                'name': name,
                'store_code': None
            }
            emails['accounts'].append(user_info)
            self.test_object.create_user(email, name, [RolesTypes.Accounts.value], True)

        for i in range(2, 5):
            name = self.test_object.fake.name()
            email = self.test_object.fake.email()
            user_info = {
                'email': email,
                'name': name,
                'store_code': None
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
                'name': name,
                'store_code': None
            }
            emails['support'].append(user_info)
            self.test_object.create_user(email, name, [RolesTypes.Support.value], True, None, None, False)

    def create_random_of_stores_users(self):
        emails = self.create_platforms_users()

        for i in range(5, 10):
            name = self.test_object.fake.name()
            email = self.test_object.fake.email()
            store_info = self.test_object.create_store(email, name)
            user_info = {
                'email': email,
                'name': name,
                'store_code': store_info.data.info.store_code
            }
            emails['stores'].append(user_info)
        return emails

    def create_3pages_platform_users(self):
        emails = {
            'accounts': [],
            'support': [],
            'stores': []
        }

        for i in range(2, 5):
            name = self.test_object.fake.name()
            email = self.test_object.fake.email()
            user_info = {
                'email': email,
                'name': name,
                'store_code': None
            }
            emails['accounts'].append(user_info)
            self.test_object.create_user(email, name, [RolesTypes.Accounts.value], True)

        for i in range(58, 66):
            name = self.test_object.fake.name()
            email = self.test_object.fake.email()
            user_info = {
                'email': email,
                'name': name,
                'store_code': None
            }
            emails['support'].append(user_info)
            self.test_object.create_user(email, name, [RolesTypes.Support.value], True)
        print('Total Users {} , Total Account Users {} , Total Support Users {}'.format(
            len(emails['accounts']) + len(emails['support']),
            len(emails['accounts']),
            len(emails['support'])
        ))
        return emails

    def convert_order_by_list_string(self, order_by):
        order_by_str = ''
        for idx, item in order_by:
            for key, value in item.iteritems():
                temp = [key, value]
                order_by_str = order_by_str + '|'.join(temp)
            if idx != 0:
                order_by_str = ',' + order_by_str
        return order_by_str
