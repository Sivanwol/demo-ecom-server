from firebase import firebase
from firebase_admin import auth


def check_user(email):
    try:
        user = auth.get_user_by_email(email)
        return user
    except Exception as e:
        print(e)
        return None


def create_test_user(email, password):
    user = check_user(email)
    if user is None:
        try:
            user=auth.create_user(email=email, password=password, email_verified=True, display_name="test user")
        except Exception as e:
            print(e)
            return None
    return user

def get_user_token(email, password):
    user = firebase.FirebaseAuthentication..sign_in_with_email_and_password(email, password)