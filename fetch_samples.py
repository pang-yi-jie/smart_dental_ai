"""从服务器抓取少量样例图片用于本地测试。"""

import os

import paramiko

HOST = "172.18.6.218"
PORT = 436
USER = "pangyj"

FRONT_DIR = "/raid5/pangyj/yolov8-segment/Front_seg/images/val"
OCC_DIR = "/raid5/pangyj/yolov8-segment/OCC_DATA/images/val"

FRONT_FILES = [
    "09290335QIUSIRUI (8)_1_4.jpg",
    "09290812hantianyao (4)_2_1.jpg",
    "09290815jianyufeng (4)_1_1.jpg",
    "09290822linganghao (4)_2_1.jpg",
]
OCC_FILES = [
    "061220308U.jpg",
    "061220315d.jpg",
]

LOCAL_DIR = r"D:\SmartDentalAI\samples"


def main() -> int:
    password = os.environ.get("SSH_PASS", "")
    if not password:
        print("[FAIL] 未设置 SSH_PASS")
        return 2

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=HOST, port=PORT, username=USER, password=password,
                   timeout=25, look_for_keys=False, allow_agent=False)

    sftp = client.open_sftp()
    os.makedirs(os.path.join(LOCAL_DIR, "front"), exist_ok=True)
    os.makedirs(os.path.join(LOCAL_DIR, "occ"), exist_ok=True)

    jobs = [(FRONT_DIR, f, "front") for f in FRONT_FILES] + [(OCC_DIR, f, "occ") for f in OCC_FILES]

    for remote_dir, name, sub in jobs:
        remote = f"{remote_dir}/{name}"
        local = os.path.join(LOCAL_DIR, sub, name)
        try:
            sftp.get(remote, local)
            size = os.path.getsize(local)
            print(f"[OK]   {sub}/{name}  ({size / 1024:.0f} KB)")
        except Exception as exc:  # noqa: BLE001
            print(f"[FAIL] {sub}/{name}: {exc}")

    sftp.close()
    client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
