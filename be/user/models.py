# user/models.py

from db import db
from enum import Enum
from sqlalchemy import Enum as EnumType

class UserStatus(Enum):
    inactive = 'inactive'
    active = 'active'

class UserRole(Enum):
    user = 'user'
    admin = 'admin'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(EnumType(UserStatus), default=UserStatus.inactive, nullable=False)
    role = db.Column(EnumType(UserRole), default=UserRole.user, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "status": self.status.value,
            "role": self.role.value,
        }


    def update_role(self, new_role):
        if new_role in [role.value for role in UserRole]:
            self.role = UserRole(new_role)
        else:
            raise ValueError("Invalid role value")

    def update_status(self, new_status):
        if new_status in [status.value for status in UserStatus]:
            self.status = UserStatus(new_status)
        else:
            raise ValueError("Invalid status value")