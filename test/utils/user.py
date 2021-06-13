from src.utils.enums import RolesTypes


class UserTestUtills:
    def __init__(self, test_object):
        self.test_object = test_object

    def create_platforms_users(self):
        emails = {
            'accounts': [],
            'support': [],
            'stores': [],
            'stores_staff': []
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

    def create_store_users(self):
        emails = self.create_platforms_users()
        name = self.test_object.fake.name()
        email = self.test_object.fake.email()
        store_info = self.test_object.create_store(email, name)
        user_info = {
            'email': email,
            'name': name,
            'store_code': store_info.data.info.store_code
        }
        emails['stores'].append(user_info)
        for i in range(5):
            name = self.test_object.fake.name()
            email = self.test_object.fake.email()
            self.test_object.create_user(email, name, [RolesTypes.StoreSupport.value], False, store_info.data.info.store_code)
            user_info = {
                'email': email,
                'name': name,
                'store_code': store_info.data.info.store_code
            }
            emails['stores_staff'].append(user_info)

        return emails

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
            'stores': [],
            'stores_staff': []
        }

        for i in range(2, 5):
            name = self.test_object.fake.name()
            email = self.test_object.fake.email()
            user_info = {
                'email': email,
                'name': name,
                'store_code': None
            }
            self.test_object.create_user(email, name, [RolesTypes.Accounts.value], True)
            emails['accounts'].append(user_info)

        for r in range(53):
            try:
                name = self.test_object.fake.name()
                email = self.test_object.fake.email()
                user_info = {
                    'email': email,
                    'name': name,
                    'store_code': None
                }
                self.test_object.create_user(email, name, [RolesTypes.Support.value], True)
                emails['support'].append(user_info)
            except:
                pass
        print('Total Users {} , Total Account Users {} , Total Support Users {}'.format(
            len(emails['accounts']) + len(emails['support']),
            len(emails['accounts']),
            len(emails['support'])
        ))
        return emails

    def convert_order_by_list_string(self, order_by):
        order_by_str = ''
        i = 0
        while i < len(order_by):
            object_mapping = []
            for key, value in order_by[i].items():
                object_mapping.append(value)
            order_by_str = order_by_str + '|'.join(object_mapping)

            order_by_str += ","
            i += 1
        return order_by_str[:-1]
