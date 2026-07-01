"""
Pipeline: calls accept_audio.py -> convert_to_wav.py -> transcribe_with_timestamps.py
"""

import argparse
import os
import subprocess
import sys
import tempfile


SCRIPTS = {
    "accept":     "accept_audio.py",
    "convert":    "convert_to_wav.py",
    "transcribe": "transcribe_longaudios.py",
}


def run_script(script: str, *args) -> str:
    result = subprocess.run(
        [sys.executable, script, *args],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"{script} failed:\n{result.stderr.strip()}")
    return result.stdout.strip()


def main():
    parser = argparse.ArgumentParser(description="Full transcription pipeline.")
    parser.add_argument("audio_path", help="Path to supported audio file")
    parser.add_argument("--model", default="base",
                        choices=["tiny", "base", "small", "medium", "large-v3", "large-v3-turbo"])
    args = parser.parse_args()

    # convert_to_wav.py auto-derives output as <name>_converted.wav
    converted_path = os.path.splitext(args.audio_path)[0] + "_converted.wav"

    try:
        print("[1/3] Validating...", file=sys.stderr)
        run_script(SCRIPTS["accept"], args.audio_path)

        print("[2/3] Converting...", file=sys.stderr)
        run_script(SCRIPTS["convert"], args.audio_path)

        print("[3/3] Transcribing...", file=sys.stderr)
        result = run_script(SCRIPTS["transcribe"], converted_path, "--model", args.model)
        print(result)

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if os.path.exists(converted_path):
            os.unlink(converted_path)


if __name__ == "__main__":
    main()
