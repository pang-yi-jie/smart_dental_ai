"""YOLOv8 检测模型测试脚本：OCC（咬合面）+ Front（唇颊面）

用法示例:
    python test_detection.py                      # 默认用 test.jpg + 两个模型
    python test_detection.py --image 某张图.jpg
    python test_detection.py --only occ            # 只测咬合面模型
    python test_detection.py --only front --conf 0.4
    python test_detection.py --imgsz 640
"""

import argparse
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:  # noqa: BLE001
    pass

BASE = Path(__file__).resolve().parent
PROJECT = BASE / "yolov8-segment"

# 训练产物中定位到的两个模型（经实测筛选）
#   OCC  : det_occ.yaml, 12 类(A~E,1~7), mAP50=0.96
#   Front: det_front2.yaml, 2 类(B/C), 实测 train174 最优
DEFAULT_OCC = PROJECT / "runs" / "detect" / "train176" / "weights" / "best.pt"
DEFAULT_FRONT = PROJECT / "runs" / "detect" / "train174" / "weights" / "best.pt"

# 两个模型训练时都是 imgsz=384，推理保持一致效果最好
DEFAULT_IMGSZ = 384


def run_model(model_path: Path, tag: str, image: Path, conf: float,
              img_size, out_dir: Path):
    from ultralytics import YOLO

    print()
    print("=" * 60)
    print(f"模型: {tag}")
    print("=" * 60)

    model = YOLO(str(model_path))
    print(f"  路径  : {model_path}")
    print(f"  任务  : {model.task}")
    print(f"  类别数: {len(model.names)}")
    print(f"  类别  : {model.names}")

    kwargs = {"conf": conf, "verbose": False}
    if img_size:
        kwargs["imgsz"] = img_size

    result = model.predict(str(image), **kwargs)[0]

    print(f"\n  输入图片: {image}")
    print(f"  原图尺寸: {result.orig_shape}")
    print(f"  检测数量: {len(result.boxes)}")

    if len(result.boxes) == 0:
        print("  （未检测到目标，可尝试降低 --conf）")

    for idx, box in enumerate(result.boxes, 1):
        cls_id = int(box.cls[0])
        cls_name = model.names[cls_id]
        score = float(box.conf[0])
        x1, y1, x2, y2 = [round(float(v), 1) for v in box.xyxy[0].tolist()]
        print(f"    #{idx:<3} 类别={cls_name:<6} conf={score:.3f}  box=({x1}, {y1}, {x2}, {y2})")

    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{tag}_{image.stem}_pred.jpg"
    result.save(filename=str(out_file))
    print(f"\n  标注图已保存: {out_file}")

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="YOLOv8 OCC / Front 检测模型测试")
    parser.add_argument("--image", default=str(PROJECT / "test.jpg"), help="输入图片路径")
    parser.add_argument("--occ", default=str(DEFAULT_OCC), help="OCC 咬合面模型路径")
    parser.add_argument("--front", default=str(DEFAULT_FRONT), help="Front 唇颊面模型路径")
    parser.add_argument("--conf", type=float, default=0.25, help="置信度阈值")
    parser.add_argument("--imgsz", type=int, default=DEFAULT_IMGSZ,
                        help=f"推理尺寸（默认 {DEFAULT_IMGSZ}，与训练一致）")
    parser.add_argument("--only", choices=["occ", "front", "both"], default="both")
    parser.add_argument("--out-dir", default=str(BASE / "outputs"), help="标注图输出目录")
    args = parser.parse_args()

    image = Path(args.image)
    if not image.exists():
        print(f"[FAIL] 图片不存在: {image}")
        return 1

    targets = []
    if args.only in ("occ", "both"):
        targets.append(("OCC_咬合面", Path(args.occ)))
    if args.only in ("front", "both"):
        targets.append(("Front_唇颊面", Path(args.front)))

    for _, path in targets:
        if not path.exists():
            print(f"[FAIL] 模型不存在: {path}")
            return 1

    out_dir = Path(args.out_dir)
    for tag, path in targets:
        run_model(path, tag, image, args.conf, args.imgsz, out_dir)

    print("\n完成。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
