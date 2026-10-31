"""在阿里云上直接下载并安装 frps（不经过本地，避免 Windows 杀软拦截）。

密码从环境变量 SSH_PASS 读取。
"""

import os
import time

import paramiko

HOST = "8.148.239.149"
PORT = 22
USER = "root"
TOKEN = "D3ntalFrp@2026#Tunnel"
VER = "0.71.1"
FRP_DIR = "/usr/local/frp"
URL = f"https://github.com/fatedier/frp/releases/download/v{VER}/frp_{VER}_linux_amd64.tar.gz"
MIRROR = f"https://gh-proxy.com/{URL}"  # 备选镜像（GitHub 慢时用）


def run(c, cmd, timeout=600):
    _i, o, e = c.exec_command(cmd, timeout=timeout)
    return o.read().decode("utf-8", "replace"), e.read().decode("utf-8", "replace"), o.channel.recv_exit_status()


def main() -> int:
    pw = os.environ.get("SSH_PASS", "")
    if not pw:
        print("[FAIL] 未设置 SSH_PASS")
        return 2

    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(HOST, PORT, USER, pw, timeout=30, look_for_keys=False, allow_agent=False)
    print("[OK] 已连接阿里云")

    print("[1/4] 下载 frp（GitHub 直连）")
    o, e, code = run(c, f"curl -L --connect-timeout 20 -o /tmp/frp.tar.gz '{URL}' && ls -l /tmp/frp.tar.gz")
    if code != 0:
        print("      直连失败，换镜像...")
        o, e, code = run(c, f"curl -L --connect-timeout 20 -o /tmp/frp.tar.gz '{MIRROR}' && ls -l /tmp/frp.tar.gz")
    if code != 0:
        print(f"[FAIL] 下载失败\n{o}\n{e}")
        c.close()
        return 1
    print("      " + (o or e).strip())

    print("[2/4] 解压安装")
    cmds = [
        f"mkdir -p {FRP_DIR}",
        f"tar -xzf /tmp/frp.tar.gz -C /tmp",
        f"cp -f /tmp/frp_{VER}_linux_amd64/frps {FRP_DIR}/frps",
        f"chmod +x {FRP_DIR}/frps",
    ]
    for cmd in cmds:
        o, e, code = run(c, cmd)
        if code != 0:
            print(f"[FAIL] {cmd}\n{e}")
            c.close()
            return 1

    print("[3/4] 写 frps.toml（通过 SFTP，文本直写）")
    conf = f'bindPort = 7000\nauth.token = "{TOKEN}"\n'
    sftp = c.open_sftp()
    with sftp.open(f"{FRP_DIR}/frps.toml", "w") as f:
        f.write(conf)
    sftp.close()

    print("[4/4] 启动 frps")
    run(c, "pkill -f frps || true")
    run(c, f"nohup {FRP_DIR}/frps -c {FRP_DIR}/frps.toml > /var/log/frps.log 2>&1 &")
    time.sleep(3)
    o, e, code = run(c, "ss -tlnp | grep 7000 || echo '端口未监听'")
    print("      监听:", (o or e).strip())
    o, e, code = run(c, "tail -8 /var/log/frps.log")
    print("      日志:\n" + (o or e).strip())

    c.close()
    print("\n[DONE] frps 安装启动完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
