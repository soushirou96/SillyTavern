# Quick Start Guide - Gemini Video Transcriber

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install google-generativeai
```

Or use the requirements file:
```bash
pip install -r requirements-transcriber.txt
```

### Step 2: Get Your Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

### Step 3: Run the Application

**Windows:**
```bash
python video_transcriber.py
```
Or double-click: `start_transcriber.bat`

**Linux/Mac:**
```bash
python3 video_transcriber.py
```
Or run: `./start_transcriber.sh`

## 📝 First Time Setup

1. **Add Your API Key**
   - Click "Manage Keys" button
   - Click "Add New Key"
   - Name it (e.g., "My Key")
   - Paste your API key
   - Click "Save"

2. **Select Your Video**
   - Click "Browse" under Video File
   - Choose your video

3. **Pick Output Location**
   - Original folder: SRT saves next to video
   - Custom folder: Choose any folder

4. **Click "Start Transcription"**
   - Watch progress bar
   - Done! Your SRT file is ready

## 💡 Common Use Cases

### Transcribe English Video
Keep the default prompt and click "Start Transcription"

### Translate Spanish to English
Change prompt to:
```
Transcribe this video and translate all speech from Spanish to English. Format as SRT with timestamps.
```

### Add Speaker Labels
Change prompt to:
```
Transcribe with speaker labels (Speaker 1, Speaker 2, etc.) in SRT format with timestamps.
```

## ⚙️ Settings Explained

- **Temperature (0-2)**: 
  - 0-0.3: Very precise, deterministic
  - 0.7: Balanced (default)
  - 1.5-2.0: More creative, varied

- **Output Mode**:
  - Original folder: Convenient for single videos
  - Custom folder: Better for batch processing

## 🔧 Troubleshooting

**"No video selected"**
→ Click Browse and select a video file

**"Please select an API key"**
→ Add an API key via "Manage Keys"

**"Transcription error"**
→ Check your API key is valid
→ Ensure video format is supported (MP4, MOV, etc.)
→ Check internet connection

## 📊 Expected Processing Times

- Short video (< 5 min): 1-3 minutes
- Medium video (5-20 min): 3-8 minutes  
- Long video (20-60 min): 8-20 minutes

Times vary based on video length, complexity, and API response time.

## 🎯 Pro Tips

1. **Multiple API Keys**: Add backup keys to switch if you hit rate limits
2. **Prompt Engineering**: Be specific about what you want (language, format, style)
3. **Temperature**: Lower for factual content, higher for creative content
4. **Batch Processing**: Use custom folder mode to organize outputs

---

**Need Help?** Check the full [TRANSCRIBER_README.md](TRANSCRIBER_README.md) for detailed documentation.
