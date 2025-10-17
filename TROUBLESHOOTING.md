# Troubleshooting Guide - Video Transcriber

## 🔧 Common Issues and Solutions

### Installation Issues

#### "pip: command not found" or "pip3: command not found"
**Problem**: Python pip is not installed or not in PATH

**Solutions**:
```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install python3-pip

# On macOS with Homebrew
brew install python3

# On Windows
# Download Python from python.org and ensure "Add to PATH" is checked
```

#### "externally-managed-environment" error
**Problem**: System prevents installing packages globally

**Solution**: Create a virtual environment:
```bash
# Create virtual environment
python3 -m venv transcriber-env

# Activate it
# On Linux/Mac:
source transcriber-env/bin/activate
# On Windows:
transcriber-env\Scripts\activate

# Install dependencies
pip install -r requirements-transcriber.txt

# Run the app
python video_transcriber.py
```

#### "No module named 'tkinter'"
**Problem**: Tkinter not installed

**Solutions**:
```bash
# On Ubuntu/Debian
sudo apt install python3-tk

# On Fedora
sudo dnf install python3-tkinter

# On macOS (usually pre-installed)
# If missing, reinstall Python from python.org

# On Windows (usually pre-installed)
# If missing, reinstall Python and ensure "tcl/tk" is checked
```

---

### API Key Issues

#### "Please select an API key"
**Problem**: No API key has been added

**Solution**:
1. Click "Manage Keys" button
2. Click "Add New Key"
3. Enter a name (e.g., "My Key")
4. Paste your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
5. Click "Save"
6. Select the key from dropdown

#### "Invalid API key" or "403 Forbidden"
**Problem**: API key is incorrect or inactive

**Solutions**:
- Verify the key is copied correctly (no extra spaces)
- Check key is active in [Google AI Studio](https://makersuite.google.com/app/apikey)
- Generate a new API key if needed
- Update the key using "Manage Keys" → Remove old → Add new

#### "429 Rate Limit Exceeded"
**Problem**: Too many requests to API

**Solutions**:
- Wait a few minutes before retrying
- Add additional API keys for rotation
- Check your Gemini API quota at Google AI Studio
- Consider upgrading your API plan

#### API keys not saving
**Problem**: Permission issues or file system problems

**Solutions**:
```bash
# Check if api_keys.json exists and is writable
ls -la api_keys.json

# If permission denied, fix permissions
chmod 644 api_keys.json

# On Windows, ensure you have write access to the folder
# Right-click folder → Properties → Security
```

---

### Video Upload Issues

#### "Please select a video file"
**Problem**: No video selected or selection failed

**Solution**:
1. Click "Browse" button
2. Navigate to your video file
3. Ensure file has a video extension (.mp4, .mov, etc.)
4. Verify file is not corrupted (try playing it first)

#### "Video processing failed"
**Problem**: Video format not supported or file corrupted

**Solutions**:
- Convert video to MP4 format using FFmpeg or video converter:
  ```bash
  ffmpeg -i input.avi output.mp4
  ```
- Try a different video file to test
- Ensure video file is not DRM-protected
- Check video file size (very large files may timeout)

#### "Upload timeout" or takes too long
**Problem**: Large file size or slow internet

**Solutions**:
- Compress video before uploading:
  ```bash
  ffmpeg -i input.mp4 -vcodec libx264 -crf 23 output.mp4
  ```
- Check internet connection speed
- Try uploading during off-peak hours
- Split long videos into smaller segments

#### "Network error" during upload
**Problem**: Internet connection issue

**Solutions**:
- Check internet connectivity
- Try disabling VPN/proxy temporarily
- Check firewall isn't blocking Python
- Restart router if needed

---

### Output Issues

#### "Please select a custom output folder"
**Problem**: Custom folder mode selected but no folder chosen

**Solution**:
1. Click "Browse" button next to custom folder option
2. Select or create a folder
3. OR switch to "Original folder" mode

#### SRT file not created
**Problem**: File save permission issue

**Solutions**:
- Check you have write permission to target folder
- Ensure disk has free space
- Try saving to a different folder
- On Windows, run as Administrator if needed

#### SRT file has wrong content
**Problem**: Gemini returned text not in SRT format

**Solutions**:
- Modify prompt to explicitly request SRT format:
  ```
  Please format as SRT subtitles with this structure:
  1
  00:00:00,000 --> 00:00:05,000
  Subtitle text

  2
  00:00:05,000 --> 00:00:10,000
  Next subtitle text
  ```
- Lower temperature to 0.3-0.5 for more structured output
- Check if video actually has speech (not just music/silence)

#### Timestamps are incorrect
**Problem**: Timing doesn't match video

**Solutions**:
- Adjust prompt for more accurate timing
- Request shorter subtitle segments (3-5 seconds each)
- Try processing again with different temperature
- Remember: AI estimates timing, may not be frame-perfect

---

### Application Issues

#### Window doesn't open / Blank screen
**Problem**: GUI framework issue

**Solutions**:
```bash
# Check if tkinter works
python3 -c "import tkinter; tkinter.Tk().destroy()"

# If error, reinstall tkinter
sudo apt install python3-tk  # Linux

# On macOS, reinstall Python from python.org
# On Windows, repair Python installation
```

#### "Application not responding"
**Problem**: Long processing or frozen

**Solutions**:
- Wait patiently - large videos take time
- Check progress bar for movement
- If truly frozen (5+ minutes no change):
  - Force quit application
  - Check internet connection
  - Try smaller video first
  - Check system resources (CPU/memory)

#### Progress bar stuck at certain percentage
**Problem**: Processing stage taking long time

**What's Normal**:
- 10% (Uploading): 1-10 minutes for large files
- 30% (Processing): 2-5 minutes for Gemini to process
- 50% (Transcribing): 3-15 minutes depending on length
- 90% (Finalizing): Usually quick (< 1 minute)

**If truly stuck** (no change for 10+ minutes):
- Check internet connection
- Force quit and restart
- Try smaller video file
- Check API key quota

#### Button stays disabled after error
**Problem**: Error handling didn't re-enable button

**Solution**:
- Close and reopen application
- If persistent, restart computer
- Report bug if reproducible

---

### Translation Issues

#### Translation is incorrect
**Problem**: AI misunderstood language or context

**Solutions**:
- Be more specific in prompt:
  ```
  Translate from [source language] to [target language]
  Preserve technical terms. Maintain professional tone.
  ```
- Lower temperature (try 0.3-0.5)
- Specify dialect if needed (e.g., "European Spanish" vs "Latin American Spanish")

#### Mixed languages in output
**Problem**: Video has multiple languages

**Solution**: Update prompt:
```
This video contains both English and Spanish. 
Translate all non-English content to English.
Keep English parts unchanged. Format as SRT with timestamps.
```

#### Slang/idioms translated literally
**Problem**: Cultural context lost

**Solution**: Adjust prompt:
```
Translate this video from [source] to [target].
Localize idioms and cultural references for [target] audience.
Make it sound natural, not literal word-for-word.
Format as SRT with timestamps.
```

---

### Performance Issues

#### Application is slow
**Problem**: System resources or file size

**Solutions**:
- Close other applications
- Check CPU/memory usage (Task Manager / Activity Monitor)
- Try smaller video files
- Update Python to latest version
- Ensure adequate disk space

#### Takes much longer than expected
**Problem**: Various factors

**Typical Processing Times**:
- 5-min video: 2-4 minutes
- 15-min video: 5-10 minutes  
- 30-min video: 10-20 minutes
- 60-min video: 20-40 minutes

**If slower than above**:
- Check internet speed
- Verify API key is active
- Try during different time (API load varies)
- Check Gemini API status page

---

### Platform-Specific Issues

#### macOS: "python not found"
**Solution**:
```bash
# Use python3 instead
python3 video_transcriber.py

# Or create alias
alias python=python3
```

#### macOS: "Application is from unidentified developer"
**Solution**:
- Right-click script → Open → Open anyway
- OR: System Preferences → Security → Allow

#### Windows: "Python is not recognized"
**Solution**:
1. Reinstall Python from python.org
2. Check "Add Python to PATH" during installation
3. OR add manually to PATH:
   - System Properties → Environment Variables → Path → Add Python directory

#### Linux: Permission denied on .sh file
**Solution**:
```bash
chmod +x start_transcriber.sh
./start_transcriber.sh
```

---

## 🐛 Reporting Issues

If you encounter an issue not listed here:

1. **Check Python version**: Should be 3.8+
   ```bash
   python3 --version
   ```

2. **Check dependencies installed**:
   ```bash
   pip3 list | grep google-generativeai
   ```

3. **Check error messages**: Note exact error text

4. **Gather system info**:
   - Operating system and version
   - Python version
   - Video file format and size
   - Steps to reproduce issue

---

## ✅ Quick Diagnostic Checklist

Run through this checklist if having issues:

- [ ] Python 3.8+ installed?
- [ ] `google-generativeai` package installed?
- [ ] tkinter module available?
- [ ] Valid Gemini API key added?
- [ ] Video file exists and is playable?
- [ ] Internet connection working?
- [ ] Write permission to output folder?
- [ ] Disk space available?
- [ ] No firewall blocking Python?
- [ ] Latest version of application?

---

## 🔍 Debug Mode

To run with more verbose output for debugging:

```bash
# Add debug prints
python3 video_transcriber.py 2>&1 | tee debug.log

# Check the debug.log file for detailed error info
```

---

## 📞 Getting Help

1. Review all documentation:
   - QUICKSTART.md
   - TRANSCRIBER_README.md
   - PROMPT_EXAMPLES.md
   - This troubleshooting guide

2. Check Google Gemini API documentation:
   - [Google AI Studio](https://ai.google.dev)
   - [API Status](https://status.cloud.google.com/)

3. Verify Python/tkinter basics:
   - Test with simple tkinter app
   - Verify Python environment

---

**Most issues are resolved by**:
1. Ensuring valid API key
2. Converting video to MP4
3. Using proper SRT-format prompts
4. Having stable internet connection
5. Being patient with large files

Good luck! 🎉
