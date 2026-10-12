import json
import datetime
from flask import current_app
from extensions.db import db
from models.lost_item import LostItem
from models.found_item import FoundItem
from models.match_record import MatchRecord
from services.similarity import similarity_calculator
from services.notify_service import notify


def _parse_time(time_str):
    try:
        if "T" in time_str:
            return datetime.datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        return datetime.datetime.fromisoformat(time_str)
    except Exception:
        return None


def trigger_match_for_lost(lost_id):
    lost = LostItem.query.get(lost_id)
    if not lost or lost.status != "已发布":
        return []
    threshold = current_app.config["MATCH_THRESHOLD"]
    window_days = current_app.config["MATCH_TIME_WINDOW_DAYS"]
    lost_time = _parse_time(lost.lost_time)

    candidates = FoundItem.query.filter_by(status="已发布").all()
    results = []
    for found in candidates:
        if lost_time:
            found_time = _parse_time(found.found_time)
            if found_time and abs((lost_time - found_time).days) > window_days:
                continue
        existing = MatchRecord.query.filter_by(lost_id=lost.id, found_id=found.id).first()
        if existing:
            continue
        score, dims = similarity_calculator.compute(lost, found)
        if score >= threshold:
            m = MatchRecord(
                lost_id=lost.id,
                found_id=found.id,
                similarity=score,
                dimensions=json.dumps(dims, ensure_ascii=False),
                status="待确认",
            )
            db.session.add(m)
            results.append((m, dims))
    db.session.commit()
    for m, dims in results:
        notify(m.lost_id and LostItem.query.get(m.lost_id).publisher_id, "match", f"您的失物有新的匹配，相似度{m.similarity}", "/matches")
        notify(FoundItem.query.get(m.found_id).publisher_id, "match", f"您捡到的物品有新的匹配，相似度{m.similarity}", "/matches")
    return results


def trigger_match_for_found(found_id):
    found = FoundItem.query.get(found_id)
    if not found or found.status != "已发布":
        return []
    threshold = current_app.config["MATCH_THRESHOLD"]
    window_days = current_app.config["MATCH_TIME_WINDOW_DAYS"]
    found_time = _parse_time(found.found_time)

    candidates = LostItem.query.filter_by(status="已发布").all()
    results = []
    for lost in candidates:
        if found_time:
            lost_time = _parse_time(lost.lost_time)
            if lost_time and abs((found_time - lost_time).days) > window_days:
                continue
        existing = MatchRecord.query.filter_by(lost_id=lost.id, found_id=found.id).first()
        if existing:
            continue
        score, dims = similarity_calculator.compute(lost, found)
        if score >= threshold:
            m = MatchRecord(
                lost_id=lost.id,
                found_id=found.id,
                similarity=score,
                dimensions=json.dumps(dims, ensure_ascii=False),
                status="待确认",
            )
            db.session.add(m)
            results.append((m, dims))
    db.session.commit()
    for m, dims in results:
        notify(LostItem.query.get(m.lost_id).publisher_id, "match", f"您的失物有新的匹配，相似度{m.similarity}", "/matches")
        notify(FoundItem.query.get(m.found_id).publisher_id, "match", f"您捡到的物品有新的匹配，相似度{m.similarity}", "/matches")
    return results


def invalidate_matches(lost_id=None, found_id=None):
    query = MatchRecord.query.filter_by(status="待确认")
    if lost_id:
        query = query.filter_by(lost_id=lost_id)
    if found_id:
        query = query.filter_by(found_id=found_id)
    for m in query.all():
        m.status = "已失效"
    db.session.commit()