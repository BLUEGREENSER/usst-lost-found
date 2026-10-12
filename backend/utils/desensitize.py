def desensitize_phone(phone: str) -> str:
    if not phone or len(phone) < 7:
        return phone
    return phone[:3] + "****" + phone[-4:]


def desensitize_email(email: str) -> str:
    if not email or "@" not in email:
        return email
    local, domain = email.split("@", 1)
    if len(local) <= 2:
        return local[0] + "*" + "@" + domain
    return local[:2] + "*" * (len(local) - 2) + "@" + domain


def desensitize_student_id(sid: str) -> str:
    if not sid or len(sid) < 4:
        return sid
    return sid[:2] + "*" * (len(sid) - 4) + sid[-2:]


def desensitize_name(name: str) -> str:
    if not name:
        return name
    if len(name) <= 1:
        return name
    return name[0] + "*" * (len(name) - 1)