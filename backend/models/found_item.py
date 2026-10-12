import datetime
from extensions.db import db


class FoundItem(db.Model):
    __tablename__ = "found_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    found_time = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False, default="")
    custody = db.Column(db.Text, nullable=False, default="本人保管")
    contact_visibility = db.Column(db.Text, nullable=False, default="仅匹配可见")
    image_urls = db.Column(db.Text, nullable=False, default="[]")
    status = db.Column(db.Text, nullable=False, default="待审核")
    created_at = db.Column(db.Text, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    updated_at = db.Column(db.Text, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self):
        import json
        return {
            "id": self.id,
            "publisher_id": self.publisher_id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "found_time": self.found_time,
            "location": self.location,
            "custody": self.custody,
            "contact_visibility": self.contact_visibility,
            "image_urls": json.loads(self.image_urls) if self.image_urls else [],
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }