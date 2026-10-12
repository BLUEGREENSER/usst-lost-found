import datetime
from extensions.db import db


class ClaimRecord(db.Model):
    __tablename__ = "claim_records"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    match_id = db.Column(db.Integer, db.ForeignKey("match_records.id"), nullable=False)
    loser_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    finder_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    verify_code_hash = db.Column(db.Text, nullable=False)
    code_salt = db.Column(db.Text, nullable=False)
    code_status = db.Column(db.Text, nullable=False, default="已生成")
    code_expire_at = db.Column(db.Text, nullable=False)
    error_count = db.Column(db.Integer, nullable=False, default=0)
    lock_until = db.Column(db.Text, nullable=True)
    resend_count = db.Column(db.Integer, nullable=False, default=0)
    resend_window_start = db.Column(db.Text, nullable=True)
    status = db.Column(db.Text, nullable=False, default="进行中")
    created_at = db.Column(db.Text, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    completed_at = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "match_id": self.match_id,
            "loser_id": self.loser_id,
            "finder_id": self.finder_id,
            "code_status": self.code_status,
            "code_expire_at": self.code_expire_at,
            "error_count": self.error_count,
            "lock_until": self.lock_until,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }