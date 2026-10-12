import datetime
from extensions.db import db


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_type = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Text, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())