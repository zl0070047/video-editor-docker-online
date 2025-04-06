# Video Editor

A simple video editing tool with Mac skeuomorphic UI design, built using Python and PyQt6.

## Features

- Video import with size limit (<100MB)
- Video preview and timeline
- Video trimming and export
- GIF creation
- Customizable export settings:
  - Video format (MP4, MOV, AVI)
  - Resolution (Original, 720p, 480p)
  - Frame rate (Original, 30, 24, 15)
  - GIF-specific options

## Requirements

- Python 3.8 or higher
- FFmpeg
- PyQt6
- MoviePy
- Pillow
- NumPy

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/video-editor.git
cd video-editor
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Install FFmpeg:
- On macOS: `brew install ffmpeg`
- On Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)
- On Linux: `sudo apt-get install ffmpeg`

## Usage

1. Run the application:
```bash
python src/main.py
```

2. Import a video file using the "Import Video" button
3. Use the timeline to select the portion of the video you want to export
4. Configure export settings in the sidebar
5. Click "Export" to save the edited video or create a GIF

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 