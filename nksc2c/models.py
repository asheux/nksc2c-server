import enum
import random

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from create_app import app


db = SQLAlchemy(app)

class StatusEnum(enum.Enum):
    PENDING = 'pending'
    GOOD = 'good'
    APPROVED = 'approved'
    UNAPPROVED = 'unapproved'

class NKS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    name = db.Column(db.String(100), default="Anonymous")
    social_link = db.Column(db.String(256), nullable=True)
    notebook_name = db.Column(db.String(100), nullable=False)
    notebook_link = db.Column(db.String(1000), nullable=True)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.PENDING)
    notebook_chapter = db.Column(db.String(100), nullable=False)
    upload_token = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<NKSC2C {self.name}>'

    def generate_upload_token(self) -> str:
        token = ""
        for i in range(6):
            r = random.randint(0, 9)
            token += f"{r}"
        return token

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'created_at': self.created_at,
            'name': self.name,
            'social_link': self.social_link,
            'status': self.status.value,
            'notebook_name': self.notebook_name,
            'notebook_link': self.notebook_link,
            'notebook_chapter': self.notebook_chapter,
        }
