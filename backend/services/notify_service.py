from flask import current_app
from extensions.db import db
from models.user import User
from models.notification import Notification


class Notifier:
    def send(self, recipient_id, ntype, summary, target_url=""):
        raise NotImplementedError


class InAppNotifier(Notifier):
    def send(self, recipient_id, ntype, summary, target_url=""):
        user = User.query.get(recipient_id)
        if not user or user.status != "active":
            current_app.logger.info(f"跳过向非active用户{recipient_id}发送通知")
            return False
        n = Notification(
            recipient_id=recipient_id,
            type=ntype,
            summary=summary,
            target_url=target_url,
        )
        db.session.add(n)
        db.session.commit()
        return True


notifier = InAppNotifier()


def notify(recipient_id, ntype, summary, target_url=""):
    return notifier.send(recipient_id, ntype, summary, target_url)