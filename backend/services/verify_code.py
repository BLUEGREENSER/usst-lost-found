import datetime
from flask import current_app
from extensions.db import db
from models.claim_record import ClaimRecord
from utils.security import generate_verify_code, hash_password, verify_password


def _now():
    return datetime.datetime.now(datetime.timezone.utc)


def _parse_time(time_str):
    if not time_str:
        return None
    try:
        return datetime.datetime.fromisoformat(time_str.replace("Z", "+00:00"))
    except Exception:
        return None


def generate_and_store_code(claim_id):
    claim = ClaimRecord.query.get(claim_id)
    if not claim:
        return None
    length = current_app.config["VERIFY_CODE_LENGTH"]
    expire_hours = current_app.config["VERIFY_CODE_EXPIRE_HOURS"]

    for _ in range(10):
        code = generate_verify_code(length)
        pwd_hash, salt = hash_password(code)
        claim.verify_code_hash = pwd_hash
        claim.code_salt = salt
        claim.code_status = "已生成"
        claim.code_expire_at = (_now() + datetime.timedelta(hours=expire_hours)).isoformat()
        claim.error_count = 0
        claim.lock_until = None
        db.session.commit()
        return code
    return None


def verify_code(claim_id, code_input):
    claim = ClaimRecord.query.get(claim_id)
    if not claim:
        return False, 10004, "认领记录不存在"
    if claim.status != "进行中":
        return False, 10007, "认领状态不允许"
    if claim.code_status != "已生成":
        return False, 10009, "校验码已失效"

    now = _now()
    lock_until = _parse_time(claim.lock_until)
    if lock_until and now < lock_until:
        return False, 10008, f"校验码锁定中，请{int((lock_until - now).total_seconds() // 60)}分钟后重试"

    expire_at = _parse_time(claim.code_expire_at)
    if expire_at and now > expire_at:
        claim.code_status = "已失效"
        db.session.commit()
        return False, 10009, "校验码已过期"

    if not verify_password(code_input, claim.verify_code_hash, claim.code_salt):
        claim.error_count += 1
        max_retry = current_app.config["VERIFY_CODE_MAX_RETRY"]
        if claim.error_count >= max_retry:
            claim.lock_until = (now + datetime.timedelta(minutes=current_app.config["VERIFY_CODE_LOCK_MINUTES"])).isoformat()
            claim.error_count = 0
        db.session.commit()
        return False, 10009, "校验码错误"

    return True, 0, "成功"


def check_resend_limit(claim_id):
    claim = ClaimRecord.query.get(claim_id)
    if not claim:
        return False
    limit = current_app.config["VERIFY_CODE_RESEND_LIMIT"]
    now = _now()
    window_start = _parse_time(claim.resend_window_start)
    if not window_start or (now - window_start).total_seconds() > 3600:
        claim.resend_count = 0
        claim.resend_window_start = now.isoformat()
    if claim.resend_count >= limit:
        return False
    claim.resend_count += 1
    db.session.commit()
    return True