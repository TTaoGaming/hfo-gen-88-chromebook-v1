# Medallion: Bronze | Mutation: 0% | HIVE: V
"""
Extract MediaPipe gesture results from a video clip and emit JSONL frames
compatible with Omega Gen5 mock-replay harness.
"""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from typing import Any, Dict, List

import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions


@dataclass
class CategoryOut:
    categoryName: str
    score: float


def _cats_to_out(cats: List[Any]) -> List[Dict[str, Any]]:
    return [asdict(CategoryOut(categoryName=c.category_name, score=float(c.score))) for c in cats]


def _landmarks_to_out(landmarks: List[Any]) -> List[Dict[str, float]]:
    return [{"x": float(l.x), "y": float(l.y), "z": float(l.z)} for l in landmarks]


def _result_to_frame(result: Any) -> Dict[str, Any]:
    return {
        "landmarks": [_landmarks_to_out(lms) for lms in (result.hand_landmarks or [])],
        "gestures": [_cats_to_out(cats) for cats in (result.gestures or [])],
        "handedness": [_cats_to_out(cats) for cats in (result.handedness or [])],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to video clip (.mp4/.webm)")
    parser.add_argument("--output", required=True, help="Path to output JSONL")
    parser.add_argument(
        "--model",
        default=os.path.join(
            os.getcwd(),
            "hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/lib/mediapipe/gesture_recognizer.task",
        ),
        help="Path to MediaPipe gesture_recognizer.task",
    )
    parser.add_argument("--max-frames", type=int, default=0, help="Optional frame cap")
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video: {args.input}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)

    options = vision.GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path=args.model),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,
    )

    recognizer = vision.GestureRecognizer.create_from_options(options)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(json.dumps({
            "type": "meta",
            "fps": fps,
            "frame_count": total,
            "source": args.input,
        }) + "\n")

        frame_index = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if args.max_frames and frame_index >= args.max_frames:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            timestamp_ms = int((frame_index / fps) * 1000)
            result = recognizer.recognize_for_video(mp_image, timestamp_ms)

            f.write(json.dumps({
                "type": "frame",
                "frame_index": frame_index,
                "timestamp_ms": timestamp_ms,
                "results": _result_to_frame(result),
            }) + "\n")
            frame_index += 1

    cap.release()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
