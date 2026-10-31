"""通用 SSH 执行工具：在服务器上执行命令。

用法:
    set SSH_PASS=xxxx
    python ssh_exec.py "命令1" "命令2" ...

密码从环境变量 SSH_PASS 读取；主机/端口/用户可选环境变量：
    SSH_HOST（默认 172.18.6.218）
    SSH_PORT（默认 436）
    SSH_USER（默认 pangyj）
"""

import os
import sys

import paramiko

HOST = os.environ.get("SSH_HOST", "172.18.6.218")
PORT = int(os.environ.get("SSH_PORT", "436"))
USER = os.environ.get("SSH_USER", "pangyj")


def main() -> int:
    password = os.environ.get("SSH_PASS", "")
    if not password:
        print("[FAIL] 未设置 SSH_PASS 环境变量")
        return 2

    commands = sys.argv[1:]
    if not commands:
        print("用法: python ssh_exec.py \"命令1\" \"命令2\" ...")
        return 2

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            hostname=HOST,
            port=PORT,
            username=USER,
            password=password,
            timeout=25,
            look_for_keys=False,
            allow_agent=False,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] 连接失败: {type(exc).__name__}: {exc}")
        return 1

    for cmd in commands:
        try:
            _stdin, stdout, stderr = client.exec_command(cmd, timeout=120)
            out = stdout.read().decode("utf-8", "replace").strip()
            err = stderr.read().decode("utf-8", "replace").strip()
        except Exception as exc:  # noqa: BLE001
            print(f"--- {cmd} ---\n[ERROR] {exc}\n")
            continue
        print(f"--- {cmd} ---")
        if out:
            print(out)
        if err:
            print(f"[stderr] {err}")
        print()

    client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
