# MP3 Edit Desktop App

# Introduction

MP3 Edit is a robust Python desktop application designed for advanced audio manipulation and playback.
It allows users to create multiple music players, apply various audio filters, and use an equalizer for sound adjustments, among other features.

# Preview

[![Preview](https://i.imgur.com/cNNXYrC.png)](https://i.imgur.com)

# Features

- **Multiple Music Players**: Create and manage several players with individual playlists.
- **Advanced Audio Filters**: Includes LowPass, HighPass, Echo, Reverb, and Flanger.
- **Audio Equalizer**: Control frequency bands from 62Hz to 16kHz.
- **Playback Delay**: Set different delays for each player to manage sound playback timing.
- **Silence Detection**: Automatically detect and analyze silence within audio tracks.
- **Audio Export**: Export audio from one or all players simultaneously.
- **Audio Recording and YouTube Downloads**: Record sounds or download directly from YouTube.
- **Leap AI Music Generation**: Generate music using Leap AI, provided you have an API key.
- **Graphical Analysis**: Visualize various audio properties and behaviors.
- **Project Management**: Save and manage project settings and data.

# Technology Stack

Below is a concise list of the main libraries used and one-sentence descriptions of what they do in this project:

- Python: primary programming language used to implement the application logic.
- PySide6: provides the Qt-based desktop GUI (windows, widgets, dialogs, timers) used across `views/` and `controllers/`.
- numpy: numerical array library used for signal processing and math operations on audio data.
- matplotlib: plotting library used to render waveforms, spectrograms and other visualizations.
- pydub: high-level audio file manipulation (loading, slicing, exporting) and format handling via FFmpeg.
- librosa: music/audio analysis (feature extraction, beat tracking, spectrograms) for visualizers and segmentation.
- scipy: scientific computing functions used for DSP operations and filters.
- pygame: audio playback and queue management utilities used by some player implementations.
- pytube: download audio/video content from YouTube for import into the app.
- pillow (PIL): image handling for icons and conversions (used with Qt via ImageQt).
- pyaudio: real-time audio input/output (microphone recording) via PortAudio bindings.
- requests: HTTP client used by AI integrations and external API calls.
- ffmpeg (external tool): system-level encoder/decoder required by `pydub` for many audio formats (install separately and add to PATH).

# Architecture

A short overview of the application's architecture:

- Layered design: the UI layer (`views/` + `controllers/`) is separated from the core logic (`cores/`) and domain models (`models/`).
- Models and services: audio I/O, processing and player implementations live in `models/` (subpackages: `audio_io`, `audio_edit`, `mp3_players`, `visualizers`).
- Controllers: `controllers/` orchestrate UI actions, background processing and interactions with `cores/` and `models/`.
- Extensibility: new players, filters or visualizers can be added by following existing `models/*` interfaces; AI integrations and external downloaders are encapsulated under `models/audio_io` and `tools/`.

# Getting Started

1. Clone the repository:

```bash
git clone https://github.com/unewMe/mp3_edit-web-app
```

2. Navigate to the project directory:

```
cd mp3_edit-web-app
```

3. Install requierments

```
pip install -r requirements.txt
```

4. Install ffmpeg and add it to the Path (You can do it from this website: https://www.gyan.dev/ffmpeg/builds/)

5. Run the application:

```
python main.py
```

# Contribution

Contributions are welcome! Feel free to fork the project, open issues, and submit pull requests.

# License

This project is licensed under the MIT License. See the LICENSE file for more details.

# About

This application aims to provide a comprehensive platform for audio enthusiasts and professionals to experiment with sound, offering tools for complex editing and analysis.
