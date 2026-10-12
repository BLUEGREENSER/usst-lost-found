import datetime
from extensions.db import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    type = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    target_url = db.Column(db.Text, nullable=False, default="")
    is_read = db.Column(db.Integer, nullable=False, default=0)
    is_archived = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.Text, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "summary": self.summary,
            "target_url": self.target_url,
            "is_read": bool(self.is_read),
            "created_at": self.created_at,
        }