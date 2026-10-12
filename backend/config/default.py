import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "usst-lost-found-secret-key-2026")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "instance", "lost_found.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-usst-2026")
    JWT_EXPIRE_DAYS = int(os.environ.get("JWT_EXPIRE_DAYS", "7"))

    SCHOOL_EMAIL_DOMAIN = os.environ.get("SCHOOL_EMAIL_DOMAIN", "@usst.edu.cn")

    VERIFY_CODE_LENGTH = int(os.environ.get("VERIFY_CODE_LENGTH", "6"))
    VERIFY_CODE_EXPIRE_HOURS = int(os.environ.get("VERIFY_CODE_EXPIRE_HOURS", "24"))
    VERIFY_CODE_MAX_RETRY = int(os.environ.get("VERIFY_CODE_MAX_RETRY", "5"))
    VERIFY_CODE_LOCK_MINUTES = int(os.environ.get("VERIFY_CODE_LOCK_MINUTES", "30"))
    VERIFY_CODE_RESEND_LIMIT = int(os.environ.get("VERIFY_CODE_RESEND_LIMIT", "3"))

    MATCH_THRESHOLD = float(os.environ.get("MATCH_THRESHOLD", "0.6"))
    MATCH_TIME_WINDOW_DAYS = int(os.environ.get("MATCH_TIME_WINDOW_DAYS", "7"))

    MATCH_WEIGHT_CATEGORY = float(os.environ.get("MATCH_WEIGHT_CATEGORY", "0.30"))
    MATCH_WEIGHT_NAME = float(os.environ.get("MATCH_WEIGHT_NAME", "0.35"))
    MATCH_WEIGHT_DESCRIPTION = float(os.environ.get("MATCH_WEIGHT_DESCRIPTION", "0.20"))
    MATCH_WEIGHT_LOCATION = float(os.environ.get("MATCH_WEIGHT_LOCATION", "0.15"))

    IMAGE_MAX_COUNT = int(os.environ.get("IMAGE_MAX_COUNT", "5"))
    IMAGE_MAX_SIZE_MB = int(os.environ.get("IMAGE_MAX_SIZE_MB", "5"))
    IMAGE_STORAGE_DIR = os.environ.get(
        "IMAGE_STORAGE_DIR", os.path.join(BASE_DIR, "static", "uploads")
    )
    IMAGE_URL_PREFIX = "/static/uploads"

    PAGE_SIZE_DEFAULT = int(os.environ.get("PAGE_SIZE_DEFAULT", "10"))
    PAGE_SIZE_MAX = int(os.environ.get("PAGE_SIZE_MAX", "50"))

    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@usst.edu.cn")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

    LOG_DIR = os.environ.get("LOG_DIR", os.path.join(BASE_DIR, "logs"))

    ITEM_CATEGORIES = ["电子产品", "证件", "钥匙", "书籍文具", "衣物", "钱包", "卡类", "其他"]
    CUSTODY_OPTIONS = ["本人保管", "已交失物招领处", "已交保卫处"]
    ITEM_STATUSES = ["待审核", "已发布", "已匹配", "已认领", "已关闭", "已驳回"]
    MATCH_STATUSES = ["待确认", "已确认", "已拒绝", "已失效"]
    CLAIM_STATUSES = ["进行中", "已完成", "已取消"]
    CODE_STATUSES = ["已生成", "已使用", "已失效"]
    CONTACT_VISIBILITIES = ["公开", "仅匹配可见", "仅登录可见"]