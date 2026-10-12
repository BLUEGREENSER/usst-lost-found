import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from extensions.db import db
from models.user import User
from utils.security import hash_password


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()
        admin_email = app.config["ADMIN_EMAIL"]
        admin_password = app.config["ADMIN_PASSWORD"]
        existing = User.query.filter_by(email=admin_email).first()
        if not existing:
            pwd_hash, salt = hash_password(admin_password)
            admin = User(
                student_id="admin",
                name="管理员",
                email=admin_email,
                password_hash=pwd_hash,
                salt=salt,
                role="admin",
                status="active",
            )
            db.session.add(admin)
            db.session.commit()
            print(f"管理员账号已创建: {admin_email} / {admin_password}")
        else:
            print("管理员账号已存在，跳过创建")
        print("建表完成，共 8 张表。")


if __name__ == "__main__":
    seed()