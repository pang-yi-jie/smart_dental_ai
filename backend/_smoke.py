"""冒烟测试：家校医协同后端全流程。"""

import sys
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = "http://127.0.0.1:8000"
IMG = Path(r"D:\SmartDentalAI\yolov8-segment\test.jpg")


def main() -> int:
    # 1. 管理员登录 + 开通学校/校医/医生
    r = requests.post(f"{BASE}/api/admin/login", json={"username": "13455774393", "password": "Pang0328"}, timeout=30)
    print("管理员登录", r.status_code)
    ah = {"Authorization": "Bearer " + r.json()["access_token"]}

    r = requests.post(f"{BASE}/api/admin/schools", params={"name": "测试小学"}, headers=ah, timeout=30)
    school_id = r.json()["id"]
    print("建学校", r.status_code, school_id)

    requests.post(f"{BASE}/api/admin/school-users", params={"school_id": school_id, "name": "王校医", "phone": "13700000001", "password": "123456"}, headers=ah, timeout=30)
    requests.post(f"{BASE}/api/admin/doctors", params={"name": "李医生", "phone": "13600000001", "password": "123456"}, headers=ah, timeout=30)
    print("建校医 + 医生 OK")

    # 2. 家长登录 + 建档 + 问卷 + 评估
    r = requests.post(f"{BASE}/api/auth/wechat", json={"phone": "13800138000"}, timeout=30)
    fh = {"Authorization": "Bearer " + r.json()["access_token"]}
    print("家长登录", r.status_code)

    r = requests.post(f"{BASE}/api/members", json={"role": "child", "name": "小明", "birth": "2016-06", "gender": "male", "school_id": school_id}, headers=fh, timeout=30)
    member_id = r.json()["id"]
    print("建成员(孩子)", r.status_code, member_id)

    r = requests.post(f"{BASE}/api/members/{member_id}/questionnaire", json={"answers": {"brush": "2次", "sugar": "少"}}, headers=fh, timeout=30)
    print("提交问卷", r.status_code)

    with IMG.open("rb") as f:
        img_bytes = f.read()
    r = requests.post(f"{BASE}/api/assessments", data={"member_id": member_id, "view": "occlusal"}, files={"file": ("test.jpg", img_bytes, "image/jpeg")}, headers=fh, timeout=180)
    a = r.json()
    print("建评估", r.status_code, "状态", a.get("status"), "风险", a.get("risk_level"), "检出", len(a.get("detections") or []))

    # 3. 学校登录 + 看学生
    r = requests.post(f"{BASE}/api/school/login", json={"phone": "13700000001", "password": "123456"}, timeout=30)
    sh = {"Authorization": "Bearer " + r.json()["access_token"]}
    r = requests.get(f"{BASE}/api/school/students", headers=sh, timeout=30)
    print("学校看学生", r.status_code, "数量", len(r.json()))

    # 4. 医生登录 + 看所有人 + 确认
    r = requests.post(f"{BASE}/api/doctor/login", json={"phone": "13600000001", "password": "123456"}, timeout=30)
    dh = {"Authorization": "Bearer " + r.json()["access_token"]}
    r = requests.get(f"{BASE}/api/doctor/assessments", headers=dh, timeout=30)
    print("医生看评估", r.status_code, "数量", len(r.json()))
    r = requests.post(f"{BASE}/api/doctor/assessments/{a['id']}/confirm", headers=dh, timeout=30)
    print("医生确认诊断", r.status_code, r.json())

    print("\n[PASS] 冒烟测试完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
