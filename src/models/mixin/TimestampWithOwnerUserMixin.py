from datetime import datetime

from sqlalchemy import String

from config.database import db
from src.models import User


class TimestampWithOwnerUserMixin(object):
    owner_user_uid = db.Column(String(100), db.ForeignKey(User.uid))
    owner = db.relationship(User, uselist=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
