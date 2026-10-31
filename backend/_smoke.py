"""端到端冒烟测试：验证后端整条链路（登录→建病例→AI分析→历史→管理员→商品）。"""

from pathlib import Path

from fastapi.testclient import TestClient

BASE = Path(__file__).resolve().parents[1]  # 项目根目录
IMG = BASE / "yolov8-segment" / "test.jpg"

from app.main import app  # noqa: E402


def main() -> int:
    with TestClient(app) as c:  # with 触发 lifespan：建表 + 预加载模型
        print("== 健康检查 ==")
        r = c.get("/health")
        print(r.status_code, r.json())

        print("\n== 微信登录（患者）==")
        r = c.post("/api/auth/wechat", json={"phone": "13800138000", "openid": "test-openid"})
        print(r.status_code, r.json())
        token = r.json()["access_token"]
        h = {"Authorization": f"Bearer {token}"}

        print("\n== 创建病例 + AI 分析（咬合面）==")
        with IMG.open("rb") as f:
            img_bytes = f.read()
        r = c.post(
            "/api/cases",
            data={"view": "occlusal", "tooth_position": "16"},
            files={"file": ("test.jpg", img_bytes, "image/jpeg")},
            headers=h,
        )
        body = r.json()
        print(r.status_code, "状态:", body.get("status"))
        dets = (body.get("ai_result") or {}).get("detections", [])
        print("检出数量:", len(dets))

        print("\n== 我的历史 ==")
        r = c.get("/api/my/cases", headers=h)
        print(r.status_code, "病例数:", len(r.json()))

        print("\n== 管理员登录 ==")
        r = c.post("/api/admin/login", json={"username": "admin", "password": "admin123"})
        print(r.status_code, r.json())
        ah = {"Authorization": f"Bearer {r.json()['access_token']}"}

        print("\n== 新增商品（好物推荐）==")
        r = c.post("/api/admin/products",
                   json={"category": "device", "title": "口腔检测仪", "taobao_code": "￥test￥"},
                   headers=ah)
        print(r.status_code, r.json())

        print("\n== 商品列表 ==")
        r = c.get("/api/products")
        print(r.status_code, r.json())

    print("\n[PASS] 冒烟测试完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
