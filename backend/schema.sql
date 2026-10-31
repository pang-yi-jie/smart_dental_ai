-- ============================================================
-- 家校医协同口腔健康管理小程序 —— 建表脚本（参考）
-- 实际建表由 SQLAlchemy ORM 的 Base.metadata.create_all() 完成
-- 主键自增整数，SQLite/PostgreSQL 通用
-- ============================================================

-- 1. 家庭账户（手机号唯一，地址账户级）
CREATE TABLE accounts (
    id         SERIAL PRIMARY KEY,
    phone      VARCHAR(32) NOT NULL UNIQUE,
    address    VARCHAR(256),
    openid     VARCHAR(64) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 学校
CREATE TABLE schools (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(128) NOT NULL,
    status     VARCHAR(16) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 家庭成员（父亲/母亲/孩子N/自己）
CREATE TABLE family_members (
    id         SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    role       VARCHAR(16) NOT NULL,
    name       VARCHAR(64) NOT NULL,
    birth      VARCHAR(16),
    gender     VARCHAR(8),
    school_id  INTEGER REFERENCES schools(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. 校医账号
CREATE TABLE school_users (
    id            SERIAL PRIMARY KEY,
    school_id     INTEGER NOT NULL REFERENCES schools(id),
    name          VARCHAR(64) NOT NULL,
    phone         VARCHAR(32) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. 医生账号（看所有人，只确认诊断）
CREATE TABLE doctors (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(64) NOT NULL,
    phone         VARCHAR(32) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. 评估记录
CREATE TABLE assessments (
    id         SERIAL PRIMARY KEY,
    member_id  INTEGER NOT NULL REFERENCES family_members(id),
    status     VARCHAR(16) DEFAULT 'uploaded',
    risk_level VARCHAR(8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. 档案级问卷（填一次，偶尔更新）
CREATE TABLE questionnaires (
    id         SERIAL PRIMARY KEY,
    member_id  INTEGER NOT NULL UNIQUE REFERENCES family_members(id),
    answers    JSON,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. 图片
CREATE TABLE images (
    id            SERIAL PRIMARY KEY,
    assessment_id INTEGER NOT NULL REFERENCES assessments(id),
    type          VARCHAR(16) NOT NULL,      -- upper/lower/annotated/crop
    path          VARCHAR(256) NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. 分析结果（含医生确认）
CREATE TABLE results (
    id               SERIAL PRIMARY KEY,
    assessment_id    INTEGER NOT NULL REFERENCES assessments(id),
    detections       JSON,
    classification   JSON,
    doctor_confirmed BOOLEAN DEFAULT FALSE,
    confirmed_by     INTEGER,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. 护牙计划任务
CREATE TABLE tasks (
    id         SERIAL PRIMARY KEY,
    member_id  INTEGER NOT NULL REFERENCES family_members(id),
    type       VARCHAR(16) NOT NULL,          -- care/learn/visit
    assignee   VARCHAR(32),
    status     VARCHAR(16) DEFAULT 'pending',
    next_step  VARCHAR(256),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. 家长反馈
CREATE TABLE feedbacks (
    id         SERIAL PRIMARY KEY,
    task_id    INTEGER NOT NULL REFERENCES tasks(id),
    type       VARCHAR(16) NOT NULL,          -- cannot/hard/fail
    content    VARCHAR(256),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. 科普视频
CREATE TABLE videos (
    id         SERIAL PRIMARY KEY,
    title      VARCHAR(128) NOT NULL,
    url        VARCHAR(256),
    category   VARCHAR(32),
    status     VARCHAR(8) DEFAULT 'on',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 13. 商品（好物推荐）
CREATE TABLE products (
    id          SERIAL PRIMARY KEY,
    category    VARCHAR(32) NOT NULL,
    title       VARCHAR(128) NOT NULL,
    cover_image VARCHAR(256),
    price       VARCHAR(32),
    description VARCHAR(512),
    taobao_code VARCHAR(128),
    taobao_url  VARCHAR(256),
    qr_image    VARCHAR(256),
    status      VARCHAR(8) DEFAULT 'on',
    sort_order  INTEGER DEFAULT 0,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 14. 审计日志
CREATE TABLE review_logs (
    id            SERIAL PRIMARY KEY,
    assessment_id INTEGER NOT NULL REFERENCES assessments(id),
    operator_id   INTEGER NOT NULL,
    changes       JSON NOT NULL,
    reviewed_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 15. AI 任务
CREATE TABLE ai_tasks (
    id            SERIAL PRIMARY KEY,
    assessment_id INTEGER NOT NULL REFERENCES assessments(id),
    model         VARCHAR(16) NOT NULL,
    status        VARCHAR(16) DEFAULT 'queued',
    error         VARCHAR(256),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
