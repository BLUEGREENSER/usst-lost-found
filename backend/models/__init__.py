# 统一导入所有 model，确保 SQLAlchemy metadata 注册全部表
from .user import User
from .lost_item import LostItem
from .found_item import FoundItem
from .image import Image
from .match_record import MatchRecord
from .claim_record import ClaimRecord
from .notification import Notification
from .audit_log import AuditLog

__all__ = [
    "User",
    "LostItem",
    "FoundItem",
    "Image",
    "MatchRecord",
    "ClaimRecord",
    "Notification",
    "AuditLog",
]
