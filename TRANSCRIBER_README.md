# Gemini Video Transcriber

A GUI application for transcribing and translating videos using Google's Gemini 2.5 Pro API with native video understanding.

## Features

- 🎥 **Video Transcription/Translation**: Uses Gemini 2.5 Pro's native video understanding to transcribe or translate videos
- 🔑 **API Key Management**: Save and manage multiple API keys, select which one to use
- 📁 **Flexible Output**: Choose to save SRT files in the original video folder or a custom folder
- 🎛️ **Customizable Settings**: Adjust temperature and provide custom prompts
- 📊 **Progress Tracking**: Real-time progress bar showing transcription status
- 🌍 **Multi-language Support**: Transcribe/translate from any language to any language

## Installation

1. Make sure you have Python 3.8+ installed

2. Install required dependencies:
```bash
pip install -r requirements-transcriber.txt
```

3. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Usage

1. **Start the application**:
```bash
python video_transcriber.py
```

2. **Add API Keys**:
   - Click "Manage Keys" button
   - Click "Add New Key"
   - Enter a name for the key (e.g., "Main Key", "Backup Key")
   - Paste your Gemini API key
   - Click "Save"

3. **Select Video**:
   - Click "Browse" next to "Selected Video"
   - Choose your video file (supports MP4, AVI, MOV, MKV, FLV, WMV, WEBM)

4. **Configure Output Location**:
   - Choose "Save in original video folder" to save the SRT file next to the video
   - OR choose "Save in custom folder" and browse to select a specific folder

5. **Adjust Settings**:
   - **Temperature** (0-2): Controls randomness (lower = more deterministic, higher = more creative)
   - **Prompt**: Customize how you want the video transcribed/translated
     - For transcription: "Transcribe this video with accurate timestamps in SRT format"
     - For translation: "Transcribe this video and translate it to English/Spanish/etc with timestamps in SRT format"

6. **Start Transcription**:
   - Click "Start Transcription"
   - Watch the progress bar for status updates
   - The SRT file will be saved when complete

## Example Prompts

### Basic Transcription
```
Please transcribe this video with timestamps in SRT format. Include accurate timing for each subtitle segment.
```

### Translation
```
Please transcribe this video and translate all speech to English. Format as SRT with timestamps. Maintain the original meaning and context.
```

### Detailed Transcription with Speaker Labels
```
Transcribe this video in SRT format with timestamps. If there are multiple speakers, label them as Speaker 1, Speaker 2, etc. Include all spoken words accurately.
```

### Technical Content
```
Transcribe this technical video in SRT format. Preserve all technical terms, code snippets, and specialized vocabulary accurately. Include timestamps for each subtitle segment.
```

## File Format

The application outputs standard SRT (SubRip Subtitle) format:

```
1
00:00:00,000 --> 00:00:05,000
First subtitle text here

2
00:00:05,000 --> 00:00:10,000
Second subtitle text here
```

## Supported Video Formats

- MP4
- AVI
- MOV
- MKV
- FLV
- WMV
- WEBM

## Tips

- **For better accuracy**: Use more specific prompts describing the content type
- **For long videos**: The process may take several minutes depending on video length
- **For translations**: Specify both source and target languages in the prompt
- **API Key Rotation**: Save multiple API keys to switch between them if you hit rate limits

## Troubleshooting

### "Transcription error: Video processing failed"
- The video format may not be supported
- Try converting the video to MP4 format
- Check that the video file is not corrupted

### "Please select an API key"
- You need to add at least one API key using the "Manage Keys" button

### Slow processing
- Large video files take longer to upload and process
- Consider the video length - longer videos take more time

## API Key Storage

API keys are stored locally in `api_keys.json` in the same directory as the application. Keep this file secure and don't share it.

## Requirements

- Python 3.8+
- google-generativeai library
- tkinter (usually included with Python)
- Internet connection for API calls

## License

This tool is provided as-is for use with Google's Gemini API. Follow Google's terms of service when using the API.
