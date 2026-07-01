"""
Convert any audio file to 16kHz mono WAV for transcription.
"""

import argparse
import os
import subprocess
import sys


def convert_to_wav(input_path: str) -> str:
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    output_path = os.path.splitext(input_path)[0] + "_converted.wav"

    subprocess.run([
        "ffmpeg", "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        "-f", "wav",
        output_path,
        "-y"
    ], check=True, stderr=subprocess.DEVNULL)

    if abs(_get_duration(output_path) - _get_duration(input_path)) > 1.0:
        raise ValueError("Duration mismatch after conversion — possible corrupt output.")

    return output_path


def _get_duration(path: str) -> float:
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path
    ], capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def main():
    parser = argparse.ArgumentParser(description="Convert audio to 16kHz mono WAV.")
    parser.add_argument("input_path", help="Path to the input audio file")
    args = parser.parse_args()

    try:
        out = convert_to_wav(args.input_path)
        print(f"Converted: {out}")
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
