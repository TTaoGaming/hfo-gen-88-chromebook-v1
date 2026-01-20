#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""Gen5: Convert a video clip into MediaPipe-like mock results JSONL.

Usage:
  python scripts/gen5_clip_to_mock_jsonl.py \
    --input /path/to/clip.mp4 \
    --output /path/to/output.jsonl \
    --model /path/to/gesture_recognizer.task
"""

import argparse
import json
import os
import time

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


def to_json_result(result: vision.GestureRecognizerResult, flip_handedness: bool):
    def map_category(cat):
        return {"categoryName": cat.category_name, "score": float(cat.score)}

    gestures = []
    for g_list in result.gestures:
        gestures.append([map_category(c) for c in g_list])

    handedness = []
    for h_list in result.handedness:
        mapped = [map_category(c) for c in h_list]
        if flip_handedness:
            for item in mapped:
                if item["categoryName"] == "Left":
                    item["categoryName"] = "Right"
                elif item["categoryName"] == "Right":
                    item["categoryName"] = "Left"
        handedness.append(mapped)

    def clamp(v):
        return max(0.0, min(1.0, float(v)))

    landmarks = []
    for lm_list in result.hand_landmarks:
        landmarks.append([
            {"x": clamp(lm.x), "y": clamp(lm.y), "z": float(lm.z)} for lm in lm_list
        ])

    return {
        "gestures": gestures,
        "handedness": handedness,
        "landmarks": landmarks,
    }



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--min-detect", type=float, default=0.1)
    parser.add_argument("--min-presence", type=float, default=0.1)
    parser.add_argument("--min-track", type=float, default=0.1)
    parser.add_argument("--flip-handedness", action="store_true")
    parser.add_argument("--every", type=int, default=1, help="Process every Nth frame")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(args.input)
    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        raise RuntimeError("Failed to open input video")

    if not os.path.exists(args.model):
        raise FileNotFoundError(args.model)

    base_options = python.BaseOptions(model_asset_path=args.model)
    options = vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=args.min_detect,
        min_hand_presence_confidence=args.min_presence,
        min_tracking_confidence=args.min_track,
    )

    with vision.GestureRecognizer.create_from_options(options) as recognizer, open(
        args.output, "w", encoding="utf-8"
    ) as f:
        frame_idx = 0
        start = time.time()
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame_idx += 1
            if args.every > 1 and (frame_idx % args.every != 0):
                continue

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            timestamp_ms = int((frame_idx / (cap.get(cv2.CAP_PROP_FPS) or 30)) * 1000)
            result = recognizer.recognize_for_video(mp_image, timestamp_ms)

            payload = {
                "timestamp": timestamp_ms,
                "results": to_json_result(result, args.flip_handedness),
            }
            f.write(json.dumps(payload) + "\n")

        elapsed = time.time() - start
        print(f"Wrote JSONL: {args.output} in {elapsed:.2f}s")


if __name__ == "__main__":
    main()
