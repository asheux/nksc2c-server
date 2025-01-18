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
    UNTOUCHED = 'untouched'

class NKS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    name = db.Column(db.String(100))
    social_link = db.Column(db.String(256), nullable=True)
    notebook_name = db.Column(db.String(100), nullable=True)
    notebook_link = db.Column(db.String(1000), nullable=True)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.UNTOUCHED)
    notebook_chapter = db.Column(db.String(100), nullable=True)
    upload_token = db.Column(db.String(100), nullable=True)
    pixel_data = db.Column(db.Text, nullable=True)
    page_name = db.Column(db.String(100), nullable=True)

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
            'page_name': self.page_name,
            'pixel_data': self.pixel_data,
        }
