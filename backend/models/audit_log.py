import datetime
from extensions.db import db


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.Text, nullable=False)
    target_type = db.Column(db.Text, nullable=False)
    target_id = db.Column(db.Integer, nullable=True)
    result = db.Column(db.Text, nullable=False, default="success")
    detail = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.Text, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())