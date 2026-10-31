"""CUDA 可用性实测脚本

用法:
    python test_cuda.py

说明:
    不只是检查 torch.cuda.is_available()，而是真正在 GPU 上做计算：
    1. 矩阵乘法结果与 CPU 对比，验证数值正确
    2. 矩阵乘法性能 GPU vs CPU，验证加速是否生效
    3. 小型 CNN 前向 + 反向传播，验证 cuDNN / cuBLAS 链路
    4. 显存分配情况
"""

import sys
import time

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:  # noqa: BLE001
    pass

import torch
import torch.nn as nn


def main() -> int:
    print("=" * 58)
    print("CUDA 可用性测试")
    print("=" * 58)
    print(f"torch          : {torch.__version__}")
    print(f"CUDA 编译版本   : {torch.version.cuda}")
    print(f"cuDNN          : {torch.backends.cudnn.version()}")
    print(f"CUDA 可用       : {torch.cuda.is_available()}")

    if not torch.cuda.is_available():
        print("\n[FAIL] CUDA 不可用")
        return 1

    print(f"GPU 数量        : {torch.cuda.device_count()}")
    print(f"GPU 名称        : {torch.cuda.get_device_name(0)}")
    cap = torch.cuda.get_device_capability(0)
    props = torch.cuda.get_device_properties(0)
    print(f"算力            : sm_{cap[0]}{cap[1]}")
    print(f"显存            : {props.total_memory / 1024 ** 3:.1f} GB")

    dev = torch.device("cuda:0")

    # ---------- 测试 1: 矩阵乘法正确性 ----------
    print("\n[测试 1] 矩阵乘法正确性 (512x512, GPU vs CPU)")
    n = 512
    a_cpu = torch.randn(n, n)
    b_cpu = torch.randn(n, n)
    ref = a_cpu @ b_cpu
    out = (a_cpu.to(dev) @ b_cpu.to(dev)).cpu()
    ok = torch.allclose(out, ref, rtol=1e-3, atol=1e-3)
    max_err = (out - ref).abs().max().item()
    print(f"    结果一致: {ok}   最大误差: {max_err:.2e}")
    if not ok:
        print("    [FAIL] 矩阵乘法结果与 CPU 不一致")
        return 1

    # ---------- 测试 2: 矩阵乘法性能 ----------
    print("\n[测试 2] 矩阵乘法性能 (2048x2048)")
    n = 2048
    a = torch.randn(n, n, device=dev)
    b = torch.randn(n, n, device=dev)
    a_cpu2, b_cpu2 = a.cpu(), b.cpu()

    for _ in range(3):  # warmup
        _ = a @ b
    torch.cuda.synchronize()

    t0 = time.perf_counter()
    for _ in range(5):
        _ = a @ b
    torch.cuda.synchronize()
    gpu_ms = (time.perf_counter() - t0) / 5 * 1000

    t0 = time.perf_counter()
    _ = a_cpu2 @ b_cpu2
    cpu_ms = (time.perf_counter() - t0) * 1000

    print(f"    GPU : {gpu_ms:8.2f} ms")
    print(f"    CPU : {cpu_ms:8.2f} ms")
    print(f"    加速比: {cpu_ms / gpu_ms:.1f}x")

    # ---------- 测试 3: CNN 前向 + 反向 ----------
    print("\n[测试 3] CNN 前向 + 反向传播 (验证 cuDNN)")
    model = nn.Sequential(
        nn.Conv2d(3, 16, 3, padding=1),
        nn.BatchNorm2d(16),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3, padding=1),
        nn.BatchNorm2d(32),
        nn.ReLU(),
        nn.AdaptiveAvgPool2d(1),
        nn.Flatten(),
        nn.Linear(32, 5),
    ).to(dev)

    x = torch.randn(8, 3, 128, 128, device=dev)
    y = torch.randint(0, 5, (8,), device=dev)
    criterion = nn.CrossEntropyLoss()

    t0 = time.perf_counter()
    logits = model(x)
    loss = criterion(logits, y)
    loss.backward()
    torch.cuda.synchronize()
    fwd_bwd_ms = (time.perf_counter() - t0) * 1000

    print(f"    输出形状      : {tuple(logits.shape)}")
    print(f"    loss          : {loss.item():.4f}")
    print(f"    前向+反向耗时 : {fwd_bwd_ms:.1f} ms")
    print(f"    梯度已回传    : {model[0].weight.grad is not None}")

    # ---------- 测试 4: 显存 ----------
    print("\n[测试 4] 显存占用")
    torch.cuda.synchronize()
    print(f"    已分配: {torch.cuda.memory_allocated(0) / 1024 ** 2:.1f} MB")
    print(f"    已保留: {torch.cuda.memory_reserved(0) / 1024 ** 2:.1f} MB")

    print("\n" + "=" * 58)
    print("[PASS] CUDA 工作正常，可以用于模型推理 / 训练")
    print("=" * 58)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
