import os
from flask import Flask, request
from config.development import DevelopmentConfig
from extensions.db import db
from utils.logger import setup_logger
from utils.response import fail, BizError


def create_app(config_class=None):
    app = Flask(__name__, static_folder="static", static_url_path="/static")
    app.config.from_object(config_class or DevelopmentConfig)

    os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)
    os.makedirs(app.config["IMAGE_STORAGE_DIR"], exist_ok=True)

    db.init_app(app)
    setup_logger(app)

    with app.app_context():
        from sqlalchemy import event
        @event.listens_for(db.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        _auto_init_db(app)

    _register_blueprints(app)
    _register_error_handlers(app)
    _register_health(app)
    _register_cors(app)

    return app


def _register_cors(app):
    """跨域支持：允许 GitHub Pages 前端访问后端 API"""
    @app.after_request
    def add_cors_headers(resp):
        origin = request.headers.get("Origin")
        # 允许任何来源（演示用途）；生产环境可限制为具体域名
        resp.headers["Access-Control-Allow-Origin"] = origin or "*"
        resp.headers["Access-Control-Allow-Credentials"] = "true"
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        resp.headers["Access-Control-Max-Age"] = "86400"
        return resp

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            resp = app.make_default_options_response()
            return resp


def _auto_init_db(app):
    # 导入 models 包触发所有表注册到 SQLAlchemy metadata
    import models  # noqa: F401
    db.create_all()
    from models.user import User
    from utils.security import hash_password
    admin_email = app.config["ADMIN_EMAIL"]
    admin_password = app.config["ADMIN_PASSWORD"]
    if not User.query.filter_by(email=admin_email).first():
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
        app.logger.info(f"管理员账号已自动创建: {admin_email} / {admin_password}")


def _register_blueprints(app):
    from blueprints.auth import bp as auth_bp
    from blueprints.upload import bp as upload_bp
    from blueprints.notify import bp as notify_bp
    from blueprints.lost import bp as lost_bp
    from blueprints.found import bp as found_bp
    from blueprints.match import bp as match_bp
    from blueprints.claim import bp as claim_bp
    from blueprints.search import bp as search_bp
    from blueprints.admin import bp as admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(upload_bp, url_prefix="/api/v1/upload")
    app.register_blueprint(notify_bp, url_prefix="/api/v1/notifications")
    app.register_blueprint(lost_bp, url_prefix="/api/v1/lost")
    app.register_blueprint(found_bp, url_prefix="/api/v1/found")
    app.register_blueprint(match_bp, url_prefix="/api/v1/matches")
    app.register_blueprint(claim_bp, url_prefix="/api/v1/claims")
    app.register_blueprint(search_bp, url_prefix="/api/v1/search")
    app.register_blueprint(admin_bp, url_prefix="/api/v1/admin")


def _register_error_handlers(app):
    @app.errorhandler(BizError)
    def handle_biz(e):
        return fail(e.code, e.message)

    @app.errorhandler(404)
    def handle_404(e):
        return fail(10004)

    @app.errorhandler(500)
    def handle_500(e):
        return fail(20001)


def _register_health(app):
    @app.route("/health")
    def health():
        from sqlalchemy import text
        try:
            db.session.execute(text("SELECT 1"))
            return {"status": "ok", "db": "ok"}
        except Exception:
            return {"status": "error", "db": "error"}, 500