"""AI 分析服务：两段管线（①牙位检测 → ②龋风险分类）。"""

import json
from pathlib import Path

from app.config import settings

BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_DIR = BASE_DIR / "yolov8-segment" / "runs" / "detect"

# 第一段：牙位检测模型（已有）
DETECT_MODELS = {
    "occlusal": MODEL_DIR / "train176" / "weights" / "best.pt",  # 咬合面
    "buccal": MODEL_DIR / "train174" / "weights" / "best.pt",    # 唇颊面
}


class AIService:
    """加载检测模型，按视角推理，两段管线输出风险分级。"""

    def __init__(self):
        self._models = {}

    def preload(self):
        for view in DETECT_MODELS:
            self._get_detector(view)

    def _get_detector(self, view: str):
        if view not in DETECT_MODELS:
            raise ValueError(f"未知视角: {view}，可选 {list(DETECT_MODELS)}")
        if view not in self._models:
            from ultralytics import YOLO
            path = DETECT_MODELS[view]
            if not path.exists():
                raise FileNotFoundError(f"模型不存在: {path}")
            self._models[view] = YOLO(str(path))
        return self._models[view]

    def detect(self, image_path, view: str, conf: float | None = None) -> list:
        """第一段：牙位检测。"""
        conf = conf or settings.inference_conf
        model = self._get_detector(view)
        r = model.predict(str(image_path), imgsz=settings.inference_imgsz, conf=conf, verbose=False)[0]
        return [
            {
                "tooth": model.names[int(b.cls[0])],
                "confidence": round(float(b.conf[0]), 4),
                "bbox": [round(float(v), 1) for v in b.xyxy[0].tolist()],
            }
            for b in r.boxes
        ]

    def classify(self, detections: list, questionnaire=None) -> dict:
        """第二段：龋风险分类（TODO：待接入分类模型）。"""
        # TODO: 调用分类模型，综合牙位检测 + 问卷 → 风险等级(低/中/高)
        return {
            "risk_level": None,   # low / mid / high
            "caries": None,       # 分类模型输出
            "note": "分类模型待接入",
        }

    def analyze(self, image_path, view: str, questionnaire=None, conf=None) -> dict:
        """完整两段管线：检测 → 分类 → 风险分级。"""
        detections = self.detect(image_path, view, conf)
        classification = self.classify(detections, questionnaire)
        return {
            "detections": detections,
            "classification": classification,
            "risk_level": classification.get("risk_level"),
        }

    def annotate(self, image_path, view: str, out_dir, conf=None) -> Path:
        """生成标注图。"""
        conf = conf or settings.inference_conf
        model = self._get_detector(view)
        r = model.predict(str(image_path), imgsz=settings.inference_imgsz, conf=conf, verbose=False)[0]
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / f"{Path(image_path).stem}_{view}_annotated.jpg"
        r.save(filename=str(out))
        return out


ai_service = AIService()
