import datetime
from extensions.db import db


class MatchRecord(db.Model):
    __tablename__ = "match_records"
    __table_args__ = (db.UniqueConstraint("lost_id", "found_id", name="uq_lost_found"),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lost_id = db.Column(db.Integer, db.ForeignKey("lost_items.id"), nullable=False)
    found_id = db.Column(db.Integer, db.ForeignKey("found_items.id"), nullable=False)
    similarity = db.Column(db.Float, nullable=False, default=0.0)
    dimensions = db.Column(db.Text, nullable=True)
    status = db.Column(db.Text, nullable=False, default="待确认")
    lost_confirmed = db.Column(db.Integer, nullable=False, default=0)
    found_confirmed = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.Text, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self):
        return {
            "id": self.id,
            "lost_id": self.lost_id,
            "found_id": self.found_id,
            "similarity": round(self.similarity, 4),
            "dimensions": self.dimensions,
            "status": self.status,
            "lost_confirmed": bool(self.lost_confirmed),
            "found_confirmed": bool(self.found_confirmed),
            "created_at": self.created_at,
        }