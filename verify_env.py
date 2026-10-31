"""环境自检脚本

用法（在 dental-ai 环境中）:
    python verify_env.py

检查 Python 版本、PyTorch/CUDA、ONNX Runtime 以及全部业务依赖是否可导入。
"""

import sys


def main() -> int:
    # 兼容 Windows GBK 控制台：无法编码的字符用 ? 替代，避免脚本崩溃
    try:
        sys.stdout.reconfigure(errors="replace")
    except Exception:  # noqa: BLE001
        pass

    print(f"Python     : {sys.version}")
    print(f"Executable : {sys.executable}")
    print()

    import torch
    import torchvision

    print("=== PyTorch ===")
    print(f"torch          : {torch.__version__}")
    print(f"torchvision    : {torchvision.__version__}")
    print(f"CUDA available : {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA version   : {torch.version.cuda}")
        print(f"Device         : {torch.cuda.get_device_name(0)}")
    print()

    import onnxruntime as ort

    print("=== ONNX Runtime ===")
    print(f"onnxruntime : {ort.__version__}")
    print(f"providers   : {ort.get_available_providers()}")
    print()

    print("=== 业务依赖 ===")
    modules = [
        "fastapi", "uvicorn", "pydantic", "pydantic_settings",
        "sqlalchemy", "pymysql", "alembic",
        "redis", "celery",
        "jwt", "passlib",
        "oss2",
        "cv2", "numpy", "PIL",
        "httpx", "loguru", "tenacity",
    ]
    ok, failed = [], []
    for name in modules:
        try:
            __import__(name)
            ok.append(name)
        except Exception as exc:  # noqa: BLE001
            failed.append((name, exc))

    print(f"OK ({len(ok)}): {', '.join(ok)}")
    if failed:
        print("FAILED:")
        for name, exc in failed:
            print(f"  - {name}: {exc}")
        return 1

    print("\n环境自检通过 [PASS]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
