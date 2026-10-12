from flask import jsonify

ERROR_MAP = {
    0: (200, "成功"),
    10001: (400, "参数校验失败"),
    10002: (401, "未登录或Token失效"),
    10003: (403, "无权限或账号禁用"),
    10004: (404, "资源不存在"),
    10005: (409, "资源冲突"),
    10006: (429, "限流"),
    10007: (400, "业务规则不满足"),
    10008: (403, "校验码锁定中"),
    10009: (400, "校验码错误或过期"),
    20001: (500, "服务内部异常"),
    20002: (500, "数据库异常"),
    20003: (503, "匹配计算超时"),
}


class BizError(Exception):
    def __init__(self, code=10001, message=None):
        self.code = code
        self.message = message or ERROR_MAP.get(code, (400, "未知错误"))[1]
        super().__init__(self.message)


def success(data=None, message="成功"):
    return jsonify({"code": 0, "message": message, "data": data})


def fail(code=10001, message=None):
    http_status, default_msg = ERROR_MAP.get(code, (400, "未知错误"))
    return jsonify({"code": code, "message": message or default_msg, "data": None}), http_status