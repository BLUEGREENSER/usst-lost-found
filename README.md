# 上理工校园失物招领平台

上海理工大学学生发布丢失/捡到物品的信息，系统帮忙自动匹配，失主凭校验码认领。

## 技术栈

- 前端：Vue3 + Element Plus + Pinia + Vue Router
- 后端：Flask + SQLAlchemy + SQLite
- 匹配算法：jieba 分词 + 四维加权相似度

## 快速开始

### 一键启动后端

```bash
# Windows
start-backend.bat
```

后端地址：http://localhost:5000
管理员账号：admin / admin123（也可用 admin@usst.edu.cn 登录）

### 一键启动前端

```bash
# Windows
start-frontend.bat
```

前端地址：http://localhost:5173

### 手动启动

**后端：**
```bash
cd backend
pip install -r requirements.txt
python scripts/seed.py    # 初始化数据库和管理员账号
python run.py             # 启动服务
```

**前端：**
```bash
cd frontend
npm install
npm run dev
```

## 功能清单

| 功能 | 说明 |
|------|------|
| 注册登录 | 学校邮箱(@usst.edu.cn)注册，JWT 鉴权 |
| 发布失物 | 填写物品信息+图片，提交后待审核 |
| 发布拾物 | 同失物，额外含保管方式 |
| 列表/搜索/筛选 | 按类别/时间/地点/关键词搜索，仅展示已发布 |
| 详情 | 查看物品详情，联系方式按可见性脱敏 |
| 图片上传 | 支持 jpg/png，单张≤5MB，最多5张 |
| 站内消息 | 匹配/认领/审核等事件通知，未读角标 |
| 状态管理 | 待审核→已发布→已匹配→已认领/已关闭 |
| AI 智能匹配 | 审核通过后自动匹配异类物品，相似度≥0.6 |
| 认领核验码 | 6位校验码，24h有效，核验通过完成认领 |
| 管理员审核 | 审核通过/驳回，强制下架，用户启用/禁用 |

## 物品类别

电子产品 / 证件 / 钥匙 / 书籍文具 / 衣物 / 钱包 / 卡类 / 其他

## 认领流程

1. 系统自动匹配失物与拾物（相似度≥0.6）
2. 双方确认匹配 → 状态变为"已确认"
3. 失主发起认领 → 系统生成6位校验码 → 站内消息通知双方
4. 拾到者输入校验码核验 → 认领完成，物品状态变为"已认领"

## 配置参数（可调）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| MATCH_THRESHOLD | 0.6 | 匹配相似度阈值 |
| MATCH_TIME_WINDOW_DAYS | 7 | 匹配时间窗口(天) |
| VERIFY_CODE_EXPIRE_HOURS | 24 | 校验码有效期(小时) |
| VERIFY_CODE_MAX_RETRY | 5 | 校验码最大错误次数 |
| VERIFY_CODE_LOCK_MINUTES | 30 | 锁定时长(分钟) |
| JWT_EXPIRE_DAYS | 7 | Token有效期(天) |

通过环境变量覆盖默认值，如：`set MATCH_THRESHOLD=0.5`

## 目录结构

```
usst-lost-found/
├── backend/              # 后端 Flask
│   ├── app.py            # 应用工厂
│   ├── run.py            # 启动入口
│   ├── requirements.txt
│   ├── config/           # 配置
│   ├── extensions/       # 扩展(db/jwt)
│   ├── models/           # ORM 模型(8张表)
│   ├── blueprints/       # 9个业务蓝图
│   ├── services/         # 业务服务(匹配/校验码/通知)
│   ├── middlewares/      # 中间件(鉴权/角色/审计)
│   ├── utils/            # 工具(响应/安全/脱敏/日志)
│   └── scripts/seed.py   # 初始化脚本
├── frontend/             # 前端 Vue3
│   ├── src/
│   │   ├── api/          # 请求封装
│   │   ├── components/   # 通用组件
│   │   ├── layouts/      # 布局
│   │   ├── router/       # 路由
│   │   ├── stores/       # Pinia
│   │   └── views/        # 页面
│   └── package.json
├── start-backend.bat
├── start-frontend.bat
└── README.md
```