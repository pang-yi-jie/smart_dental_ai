"""AI 推理服务：加载 OCC / Front 检测模型，按视角路由，返回结构化结果 + 标注图。

- 单例，模型预加载进显存。
- 训练/推理尺寸统一 imgsz=384。
- 结果预留 classification 字段，后续接分类模型。
"""

import json
from pathlib import Path

from app.config import settings

BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_DIR = BASE_DIR / "yolov8-segment" / "runs" / "detect"

MODELS = {
    "occlusal": MODEL_DIR / "train176" / "weights" / "best.pt",  # OCC 咬合面
    "buccal": MODEL_DIR / "train174" / "weights" / "best.pt",    # Front 唇颊面
}


class AIService:
    """加载并缓存 YOLO 检测模型，按视角推理。"""

    def __init__(self):
        self._models = {}

    def preload(self):
        """服务启动时预加载所有模型进显存。"""
        for view in MODELS:
            self._get_model(view)

    def _get_model(self, view: str):
        if view not in MODELS:
            raise ValueError(f"未知视角: {view}，可选 {list(MODELS)}")
        if view not in self._models:
            from ultralytics import YOLO
            path = MODELS[view]
            if not path.exists():
                raise FileNotFoundError(f"模型不存在: {path}")
            self._models[view] = YOLO(str(path))
        return self._models[view]

    def predict(self, image_path, view: str, conf: float | None = None) -> dict:
        """返回结构化检测结果（不保存图）。"""
        conf = conf or settings.inference_conf
        model = self._get_model(view)
        result = model.predict(str(image_path), imgsz=settings.inference_imgsz,
                               conf=conf, verbose=False)[0]
        detections = [
            {
                "label": model.names[int(box.cls[0])],
                "confidence": round(float(box.conf[0]), 4),
                "bbox": [round(float(v), 1) for v in box.xyxy[0].tolist()],
            }
            for box in result.boxes
        ]
        return {
            "view": view,
            "model": "occ_v1" if view == "occlusal" else "front_v1",
            "detections": detections,
            "classification": None,  # 未来分类模型填充
        }

    def annotate(self, image_path, view: str, out_dir, conf: float | None = None) -> Path:
        """推理并保存标注图，返回图片路径。"""
        conf = conf or settings.inference_conf
        model = self._get_model(view)
        result = model.predict(str(image_path), imgsz=settings.inference_imgsz,
                               conf=conf, verbose=False)[0]
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / f"{Path(image_path).stem}_{view}_annotated.jpg"
        result.save(filename=str(out))
        return out


# 全局单例
ai_service = AIService()


if __name__ == "__main__":
    import sys
    img = sys.argv[1] if len(sys.argv) > 1 else str(BASE_DIR / "yolov8-segment" / "test.jpg")
    view = sys.argv[2] if len(sys.argv) > 2 else "occlusal"
    print(json.dumps(ai_service.predict(img, view), ensure_ascii=False, indent=2))
