### A python-based pipeline to transcribe audio using whisper

- Python is the go-to for AI/ML tasks because of its ecosystem.
- Open source libraries are kept up-to-date
- To keep it simple and focus on the real issues at hand

_How it works:_

*1. Accept Audio*

- Takes file path from the cli
- use argparse to make cli tooling self explanatory
- Validate the file in layers:
    1. Check for supported extensions
    2. File signature checking - to ensure the file wasn't renamed with a wrong extension
    3. Use decoding libraries to check for malformed / corruped / zero duration audio files
- Validation is done thoroughly in the first step because passing the wrong file to the next step can incur compute cost / processing delays.

*2. Convert to WAV*

- Leverage the `ffmpeg` library to convert to 16kHz mono WAV
- This step is normalisation and we do it for the following reasons:
    1. The script becomes extensible to other file types
    2. whisper models are trained on 16kHz mono files. This is the standard for speech recognition. You get the most balanced result with 16kHz frequency and mono channel
    3. `ffmpeg` is the gold standard - most audio file formats can pass through this stage 

*3. Transcribe with support for long audios*

- We run open ai whisper model to transcribe. The `--model` can be changed but defaults to `small` which is best suited for normal conversations
- I considered using `pyDub` to do manual chunking for long audios. There are a few problems here:
    - It consumes too much memory because file stream needs to be copied to the RAM
    - Arbitrary chunking (for e.g., 15 mins slices) causes whisper to hallucinate - if you cut mid-sentence, the loss of context will yield duplicate results.
    - Manual chunking leads to complexity when we are trying introduce concurrency or parallelism.
- Instead, we use `faster_whisper`. This library extends whisper functionality by chunking audios by detecting audio activity:
    - This is much better because audios are only chunked when there are long pauses of activity
    - Based on benchmarks, can be up to 4x faster with better memory consumption
    - No need to reinvent the wheel
    - We can specify `num_workers` to improve concurrency. 

### How to run

- Install python3 on your machine
- Run pip3 install -r deps.txt to install depedencies. ffmpeg is also required
- Run `python3 transcribe_main.py files/meeting_minutes.mp3` (Note the final pipeline uses `faster_whisper` instead of `whisper` )