import datetime
from extensions.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Text, nullable=False, unique=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    salt = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False, default="student")
    status = db.Column(db.Text, nullable=False, default="active")
    registered_at = db.Column(db.Text, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    last_login_at = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "user_id": self.id,
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "status": self.status,
        }