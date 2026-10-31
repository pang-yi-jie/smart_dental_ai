"""完成 frps 安装（/tmp/frp1.tar.gz 已下载好）。"""

import os
import time

import paramiko

HOST = "8.148.239.149"
PORT = 22
USER = "root"
TOKEN = "D3ntalFrp@2026#Tunnel"
VER = "0.71.1"
FRP_DIR = "/usr/local/frp"


def run(c, cmd, timeout=120):
    _i, o, e = c.exec_command(cmd, timeout=timeout)
    return o.read().decode("utf-8", "replace"), e.read().decode("utf-8", "replace"), o.channel.recv_exit_status()


def main() -> int:
    pw = os.environ.get("SSH_PASS", "")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(HOST, PORT, USER, pw, timeout=30, look_for_keys=False, allow_agent=False)
    print("[OK] 已连接阿里云")

    cmds = [
        f"mkdir -p {FRP_DIR}",
        f"tar -xzf /tmp/frp1.tar.gz -C /tmp",
        f"cp -f /tmp/frp_{VER}_linux_amd64/frps {FRP_DIR}/frps",
        f"chmod +x {FRP_DIR}/frps",
    ]
    for cmd in cmds:
        o, e, code = run(c, cmd)
        if code != 0:
            print(f"[FAIL] {cmd}\n{e}")
            c.close()
            return 1

    conf = f'bindPort = 7000\nauth.token = "{TOKEN}"\n'
    sftp = c.open_sftp()
    with sftp.open(f"{FRP_DIR}/frps.toml", "w") as f:
        f.write(conf)
    sftp.close()

    run(c, "pkill -f frps || true")
    run(c, f"nohup {FRP_DIR}/frps -c {FRP_DIR}/frps.toml > /var/log/frps.log 2>&1 &")
    time.sleep(3)

    o, e, code = run(c, "ss -tlnp | grep 7000 || echo '端口未监听'")
    print("监听检查:", (o or e).strip())
    o, e, code = run(c, "tail -8 /var/log/frps.log")
    print("日志:\n" + (o or e).strip())

    c.close()
    print("\n[DONE] frps 安装启动完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
