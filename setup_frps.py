"""在阿里云服务器上安装并启动 frps（frp 服务端）。

密码从环境变量 SSH_PASS 读取。
"""

import os
import time

import paramiko

HOST = "8.148.239.149"
PORT = 22
USER = "root"

LOCAL_TAR = r"D:\devtools\_downloads\frp_0.71.1_linux_amd64.tar.gz"
REMOTE_TAR = "/tmp/frp.tar.gz"
FRP_DIR = "/usr/local/frp"
TOKEN = "D3ntalFrp@2026#Tunnel"  # 隧道鉴权令牌（上线前可换）


def run(client, cmd, timeout=300):
    _in, out, err = client.exec_command(cmd, timeout=timeout)
    o = out.read().decode("utf-8", "replace")
    e = err.read().decode("utf-8", "replace")
    code = out.channel.recv_exit_status()
    return code, o, e


def main() -> int:
    password = os.environ.get("SSH_PASS", "")
    if not password:
        print("[FAIL] 未设置 SSH_PASS")
        return 2

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=HOST, port=PORT, username=USER, password=password,
                   timeout=30, look_for_keys=False, allow_agent=False)
    print("[OK] 已连接阿里云")

    print("[1/4] 上传 frp 包")
    sftp = client.open_sftp()
    sftp.put(LOCAL_TAR, REMOTE_TAR)
    sftp.close()
    print("      上传完成")

    print("[2/4] 解压安装")
    cmds = [
        f"mkdir -p {FRP_DIR}",
        f"tar -xzf {REMOTE_TAR} -C /tmp",
        f"cp -f /tmp/frp_0.71.1_linux_amd64/frps {FRP_DIR}/frps",
        f"chmod +x {FRP_DIR}/frps",
    ]
    for c in cmds:
        code, out, err = run(client, c)
        if code != 0:
            print(f"[FAIL] {c}\n{err}")
            client.close()
            return 1

    print("[3/4] 写入 frps.toml")
    conf = f'bindPort = 7000\nauth.token = "{TOKEN}"\n'
    sftp = client.open_sftp()
    with sftp.open(f"{FRP_DIR}/frps.toml", "w") as f:
        f.write(conf)
    sftp.close()

    print("[4/4] 启动 frps")
    run(client, "pkill -f frps || true")
    run(client, f"nohup {FRP_DIR}/frps -c {FRP_DIR}/frps.toml > /var/log/frps.log 2>&1 &")
    time.sleep(3)

    code, out, err = run(client, "ss -tlnp | grep 7000 || echo '端口未监听'")
    print("      监听检查:", (out or err).strip())
    code, out, err = run(client, "tail -8 /var/log/frps.log")
    print("      日志:\n" + (out or err).strip())

    client.close()
    print("\n[DONE] frps 安装启动完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
