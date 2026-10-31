"""医生后台全流程测试：管理员建诊所/医生 → 医生登录 → 代测建病例 → 复核 → 定稿。"""

import requests

BASE = "http://127.0.0.1:8000"
IMG = r"D:\SmartDentalAI\yolov8-segment\test.jpg"


def main() -> int:
    # 1. 管理员登录
    r = requests.post(BASE + "/api/admin/login",
                      json={"username": "admin", "password": "admin123"}, timeout=30)
    print("管理员登录", r.status_code)
    ah = {"Authorization": "Bearer " + r.json()["access_token"]}

    # 2. 建诊所
    r = requests.post(BASE + "/api/admin/clinics", params={"name": "测试口腔诊所"},
                      headers=ah, timeout=30)
    clinic_id = r.json()["id"]
    print("建诊所", r.status_code, r.json())

    # 3. 建医生账号
    r = requests.post(BASE + "/api/admin/clinic-users",
                      json={"clinic_id": clinic_id, "name": "张医生",
                            "phone": "13900000001", "password": "123456"},
                      headers=ah, timeout=30)
    print("建医生", r.status_code, r.json())

    # 4. 医生登录
    r = requests.post(BASE + "/api/clinic/login",
                      json={"phone": "13900000001", "password": "123456"}, timeout=30)
    print("医生登录", r.status_code, r.json().get("role"), r.json().get("name"))
    dh = {"Authorization": "Bearer " + r.json()["access_token"]}

    # 5. 医生代测建病例
    with open(IMG, "rb") as f:
        r = requests.post(BASE + "/api/clinic/cases",
                          data={"phone": "13800138000", "view": "occlusal",
                                "tooth_position": "16"},
                          files={"file": ("test.jpg", f, "image/jpeg")},
                          headers=dh, timeout=180)
    case = r.json()
    dets = (case.get("ai_result") or {}).get("detections", [])
    print("代测建病例", r.status_code, "状态", case.get("status"), "检出", len(dets))

    # 6. 医生看病例列表
    r = requests.get(BASE + "/api/clinic/cases", headers=dh, timeout=30)
    print("病例列表", r.status_code, "数量", len(r.json()))

    # 7. 改诊断
    r = requests.put(BASE + f"/api/clinic/cases/{case['id']}/diagnosis",
                     json={"diagnosis": {"suggestion": "16 牙面见龋坏，建议补牙"}},
                     headers=dh, timeout=30)
    print("改诊断", r.status_code, r.json())

    # 8. 定稿
    r = requests.post(BASE + f"/api/clinic/cases/{case['id']}/finalize",
                      headers=dh, timeout=30)
    print("定稿", r.status_code, "final 有内容:", bool(r.json().get("final")))

    # 9. 网页能访问
    r = requests.get(BASE + "/web/login.html", timeout=30)
    print("医生后台网页", r.status_code, "长度", len(r.text))

    print("\n[DONE] 医生后台全流程测试完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
