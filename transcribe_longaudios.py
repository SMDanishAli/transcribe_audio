"""
Q2: Transcribe audio with timestamps using faster-whisper.
"""

import argparse
import os
import sys

from faster_whisper import WhisperModel


def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def transcribe(audio_path: str, model_size: str = "base") -> None:
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, vad_filter=True)

    print(f"Detected language: {info.language}", file=sys.stderr)
    print("\n--- Transcription ---")

    for segment in segments:
        start = format_timestamp(segment.start)
        end = format_timestamp(segment.end)
        print(f"[{start} --> {end}] {segment.text.strip()}")


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio with timestamps.")
    parser.add_argument("audio_path", help="Path to an audio file")
    parser.add_argument("--model", default="base",
                        choices=["tiny", "base", "small", "medium", "large-v3", "large-v3-turbo"])
    args = parser.parse_args()

    if not os.path.exists(args.audio_path):
        print(f"Error: file not found: {args.audio_path}", file=sys.stderr)
        sys.exit(1)

    try:
        transcribe(args.audio_path, model_size=args.model)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
