"""从服务器下载 yolov8-segment（排除数据集）到本机 D 盘。

流程:
    1. 服务器上打包 tar.gz（排除数据集目录）
    2. SFTP 下载该压缩包（带进度）
    3. 本机解压
    4. 清理服务器临时文件

密码从环境变量 SSH_PASS 读取。
"""

import os
import sys
import tarfile
import time

import paramiko

HOST = "172.18.6.218"
PORT = 436
USER = "pangyj"

REMOTE_PARENT = "/raid5/pangyj"
REMOTE_DIR_NAME = "yolov8-segment"
REMOTE_TAR = "/tmp/yolov8-segment-nodata.tar.gz"

# 这些是数据集目录，不下载
EXCLUDE_DIRS = ["EYE_DATA", "OCC_DATA", "SEG_DATA", "Front_seg"]

LOCAL_PARENT = r"D:\SmartDentalAI"
LOCAL_TAR = r"D:\SmartDentalAI\_yolov8-segment-nodata.tar.gz"


def run(client, cmd, timeout=1800):
    _stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode("utf-8", "replace")
    err = stderr.read().decode("utf-8", "replace")
    code = stdout.channel.recv_exit_status()
    return code, out, err


def main() -> int:
    password = os.environ.get("SSH_PASS", "")
    if not password:
        print("[FAIL] 未设置 SSH_PASS")
        return 2

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=HOST,
        port=PORT,
        username=USER,
        password=password,
        timeout=25,
        look_for_keys=False,
        allow_agent=False,
    )
    print("[OK] 已连接服务器")

    # ---------- 1. 服务器打包 ----------
    excludes = " ".join(f"--exclude='{REMOTE_DIR_NAME}/{d}'" for d in EXCLUDE_DIRS)
    pack_cmd = (
        f"cd {REMOTE_PARENT} && "
        f"rm -f {REMOTE_TAR} && "
        f"tar -czf {REMOTE_TAR} {excludes} {REMOTE_DIR_NAME} && "
        f"ls -l {REMOTE_TAR}"
    )
    print(f"[1/4] 服务器打包中（排除 {', '.join(EXCLUDE_DIRS)}）...")
    t0 = time.time()
    code, out, err = run(client, pack_cmd, timeout=3600)
    if code != 0:
        print(f"[FAIL] 打包失败 (exit {code})\n{out}\n{err}")
        client.close()
        return 1
    print(f"      打包完成，耗时 {time.time() - t0:.0f}s")
    print(f"      {out.strip()}")

    # ---------- 2. SFTP 下载 ----------
    sftp = client.open_sftp()
    size = sftp.stat(REMOTE_TAR).st_size
    print(f"[2/4] 开始下载，大小 {size / 1024 ** 2:.1f} MB")

    t0 = time.time()
    downloaded = 0
    last_pct = -10
    with sftp.open(REMOTE_TAR, "rb") as rf, open(LOCAL_TAR, "wb") as lf:
        while True:
            chunk = rf.read(1024 * 1024)
            if not chunk:
                break
            lf.write(chunk)
            downloaded += len(chunk)
            pct = downloaded * 100 // size
            if pct >= last_pct + 10:
                elapsed = time.time() - t0
                speed = downloaded / 1024 ** 2 / elapsed if elapsed > 0 else 0
                print(f"      {pct:3d}%  {downloaded / 1024 ** 2:7.1f} MB  {speed:6.1f} MB/s")
                last_pct = pct
    sftp.close()
    print(f"      下载完成，耗时 {time.time() - t0:.0f}s")

    # ---------- 3. 本机解压 ----------
    print(f"[3/4] 解压到 {LOCAL_PARENT}")
    os.makedirs(LOCAL_PARENT, exist_ok=True)
    with tarfile.open(LOCAL_TAR, "r:gz") as tf:
        try:
            tf.extractall(LOCAL_PARENT, filter="data")
        except TypeError:
            tf.extractall(LOCAL_PARENT)
    print("      解压完成")

    # ---------- 4. 清理 ----------
    print("[4/4] 清理临时文件")
    try:
        run(client, f"rm -f {REMOTE_TAR}")
        print("      服务器临时包已删除")
    except Exception as exc:  # noqa: BLE001
        print(f"      服务器清理失败（可手动删 {REMOTE_TAR}）: {exc}")
    client.close()

    if os.path.exists(LOCAL_TAR):
        os.remove(LOCAL_TAR)
        print("      本机临时包已删除")

    target = os.path.join(LOCAL_PARENT, REMOTE_DIR_NAME)
    print(f"\n[DONE] 目标目录: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
