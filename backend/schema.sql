-- ============================================================
-- 智能牙科 AI 检测 —— 建表脚本（参考）
-- 说明：实际建表由 SQLAlchemy ORM 的 Base.metadata.create_all() 完成，
--       本文件用于人工查阅表结构。主键为自增整数，SQLite/PostgreSQL 通用。
-- ============================================================

-- 1. 用户（个人，全局身份 = 手机号）
CREATE TABLE users (
    id         SERIAL PRIMARY KEY,
    phone      VARCHAR(32) NOT NULL UNIQUE,
    openid     VARCHAR(64) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 诊所（租户）
CREATE TABLE clinics (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(128) NOT NULL,
    status     VARCHAR(16) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 诊所操作员（登录账号）
CREATE TABLE clinic_users (
    id            SERIAL PRIMARY KEY,
    clinic_id     INTEGER NOT NULL REFERENCES clinics(id),
    name          VARCHAR(64) NOT NULL,
    phone         VARCHAR(32) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. 病例
CREATE TABLE cases (
    id             SERIAL PRIMARY KEY,
    user_id        INTEGER NOT NULL REFERENCES users(id),
    clinic_id      INTEGER REFERENCES clinics(id),
    owner_id       INTEGER REFERENCES clinic_users(id),
    tooth_position VARCHAR(16),
    view           VARCHAR(16) NOT NULL,      -- occlusal / buccal
    status         VARCHAR(16) DEFAULT 'uploaded',
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. 图片
CREATE TABLE images (
    id         SERIAL PRIMARY KEY,
    case_id    INTEGER NOT NULL REFERENCES cases(id),
    type       VARCHAR(16) NOT NULL,          -- raw / annotated
    path       VARCHAR(256) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. 诊断结果（AI 原始 / 医生修改 / 最终）
CREATE TABLE diagnoses (
    id            SERIAL PRIMARY KEY,
    case_id       INTEGER NOT NULL REFERENCES cases(id),
    ai_result     JSON,
    doctor_edited JSON,
    final         JSON,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. 报告
CREATE TABLE reports (
    id         SERIAL PRIMARY KEY,
    case_id    INTEGER NOT NULL REFERENCES cases(id),
    content    JSON,
    status     VARCHAR(16) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. 审核留痕（审计）
CREATE TABLE review_logs (
    id             SERIAL PRIMARY KEY,
    case_id        INTEGER NOT NULL REFERENCES cases(id),
    clinic_user_id INTEGER NOT NULL REFERENCES clinic_users(id),
    changes        JSON NOT NULL,
    reviewed_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. AI 任务
CREATE TABLE ai_tasks (
    id         SERIAL PRIMARY KEY,
    case_id    INTEGER NOT NULL REFERENCES cases(id),
    model      VARCHAR(16) NOT NULL,          -- occ / front
    status     VARCHAR(16) DEFAULT 'queued',
    error      VARCHAR(256),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. 商品（好物推荐，淘口令带货）
CREATE TABLE products (
    id          SERIAL PRIMARY KEY,
    category    VARCHAR(32) NOT NULL,         -- device/toothpaste/toothbrush/other
    title       VARCHAR(128) NOT NULL,
    cover_image VARCHAR(256),
    price       VARCHAR(32),
    description VARCHAR(512),
    taobao_code VARCHAR(128),
    taobao_url  VARCHAR(256),
    qr_image    VARCHAR(256),
    status      VARCHAR(8) DEFAULT 'on',      -- on / off
    sort_order  INTEGER DEFAULT 0,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
