from db import db
from enum import Enum
from sqlalchemy import Enum as EnumType
import datetime

class TaskStatus(Enum):
    pending = 'pending'
    complete = 'complete'
    
class TaskType(Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(EnumType(TaskType), default = TaskType.low, nullable=False)
    status = db.Column(EnumType(TaskStatus), default = TaskStatus.pending, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    user=db.relationship("User",backref=db.backref('tweets', lazy=True))
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type.value,
            "status": self.status.value,
            "name": self.name,
            "date": self.date.strftime('%Y-%m-%d')
        }