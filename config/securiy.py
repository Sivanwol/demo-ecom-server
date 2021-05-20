from flask_security import SQLAlchemyUserDatastore

from src.models.roles import Roles

user_datastore = SQLAlchemyUserDatastore(db, User, Roles)
security = Security(secureApp, user_datastore)