import argparse
import os
import ssl
import sys
import whisper

# FIX: Force Python to ignore the self-signed certificate error when downloading the model
ssl._create_default_https_context = ssl._create_unverified_context


def transcribe_audio(audio_path: str, model_size: str = "base") -> dict:
    """Loads the Whisper model and transcribes the audio file."""
    print(
        f"Loading Whisper '{model_size}' model... (This may take a moment)",
        file=sys.stderr,
    )

    # Available sizes: 'tiny', 'base', 'small', 'medium', 'large'
    model = whisper.load_model(model_size)

    print(f"Transcribing: {os.path.basename(audio_path)}...", file=sys.stderr)
    result = model.transcribe(audio_path)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe spoken language from an audio file into text."
    )
    parser.add_argument("audio_path", help="Path to the audio file")
    parser.add_argument(
        "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size to use (default: base)",
    )
    args = parser.parse_args()

    try:
        # Transcribe directly using the provided path
        transcription_data = transcribe_audio(
            args.audio_path, model_size=args.model
        )

        # Output Results
        print("\n--- Transcription Text ---")
        print(transcription_data["text"].strip())
        print("--------------------------")

        # Output metadata to standard error stream
        detected_lang = transcription_data.get("language", "unknown")
        print(f"\nDetected Language: {detected_lang}", file=sys.stderr)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
