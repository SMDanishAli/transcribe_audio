"""
Q1: Accept an audio file (WAV/MP3).
"""

import argparse
import os
import wave
import mutagen

SUPPORTED_EXTENSIONS = {".wav", ".mp3"}

_WAV_SIGNATURE = b"RIFF"
_MP3_SIGNATURES = (b"ID3", b"\xff\xfb", b"\xff\xf3", b"\xff\xf2")


def _check_signature(audio_path: str, ext: str) -> None:
    with open(audio_path, "rb") as f:
        header = f.read(12)

    if ext == ".wav" and not header.startswith(_WAV_SIGNATURE):
        raise ValueError(f"File has .wav extension but content is not a valid WAV (bad header): {audio_path}")
    if ext == ".mp3" and not header.startswith(_MP3_SIGNATURES):
        raise ValueError(f"File has .mp3 extension but content is not a valid MP3 (bad header): {audio_path}")


def _check_decodable(audio_path: str, ext: str) -> None:
    if ext == ".wav":
        try:
            with wave.open(audio_path, "rb") as w:
                if w.getnframes() == 0:
                    raise ValueError(f"WAV file has zero audio frames (empty/corrupt): {audio_path}")
        except (wave.Error, EOFError) as e:
            raise ValueError(f"Corrupt or unreadable WAV file: {audio_path} ({e})") from e

    elif ext == ".mp3":
        from mutagen.mp3 import MP3
        from mutagen.mp3 import HeaderNotFoundError

        try:
            audio = MP3(audio_path)
        except HeaderNotFoundError as e:
            raise ValueError(f"Corrupt or unreadable MP3 file: {audio_path} ({e})") from e
        if audio.info.length <= 0:
            raise ValueError(f"MP3 file has zero duration (empty/corrupt): {audio_path}")


def accept_audio_file(audio_path: str) -> str:
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"File not found: {audio_path}")

    ext = os.path.splitext(audio_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type '{ext}'. Supported: {sorted(SUPPORTED_EXTENSIONS)}")

    _check_signature(audio_path, ext)
    _check_decodable(audio_path, ext)

    return audio_path


def main():
    parser = argparse.ArgumentParser(description="Accept an audio file (WAV/MP3).")
    parser.add_argument("audio_path", help="Path to a WAV or MP3 file")
    args = parser.parse_args()

    path = accept_audio_file(args.audio_path)
    print(f"Accepted audio file: {path}")


if __name__ == "__main__":
    main()
