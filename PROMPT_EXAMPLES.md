# Prompt Examples for Video Transcriber

This document provides ready-to-use prompts for different transcription scenarios.

## 📝 Basic Transcription

### English Video (Default)
```
Please transcribe this video with timestamps in SRT format. Include accurate timing for each subtitle segment. Format each entry as:
1
00:00:00,000 --> 00:00:05,000
Transcribed text here

Continue this pattern for the entire video.
```

### Any Language Video
```
Transcribe this video in its original language with timestamps in SRT format. Maintain proper spelling, grammar, and punctuation. Create subtitle segments of appropriate length (typically 1-7 seconds per segment).
```

## 🌍 Translation

### Spanish to English
```
Transcribe this video and translate all Spanish speech to English. Format as SRT with accurate timestamps. Preserve the meaning and tone of the original speech. Each subtitle should be 1-7 seconds long.
```

### French to English
```
Please transcribe and translate this French video to English. Format as SRT subtitles with timestamps. Maintain natural English phrasing while staying true to the original meaning.
```

### Japanese to English
```
Transcribe this Japanese video and translate to English. Include timestamps in SRT format. Preserve cultural context and honorifics where appropriate. Format subtitles for easy reading (max 2 lines, 42 characters per line when possible).
```

### Any Language to English (Auto-detect)
```
Detect the spoken language in this video and translate everything to English. Format as SRT subtitles with timestamps. Ensure translations sound natural in English.
```

### English to Spanish
```
Transcribe this English video and translate to Spanish. Use SRT format with timestamps. Ensure proper Spanish grammar, accents, and regional neutral vocabulary.
```

## 👥 Multi-Speaker Content

### With Speaker Labels
```
Transcribe this video in SRT format with timestamps. Identify and label different speakers as [Speaker 1], [Speaker 2], etc. Format:
1
00:00:00,000 --> 00:00:05,000
[Speaker 1]: Hello everyone

2
00:00:05,000 --> 00:00:10,000
[Speaker 2]: Thank you for having me
```

### Interview Format
```
Transcribe this interview in SRT format. Label speakers as [Interviewer] and [Guest]. Include all questions and answers with accurate timestamps.
```

### Panel Discussion
```
Transcribe this panel discussion. If you can identify speakers by name, use their names. Otherwise use [Speaker 1], [Speaker 2], etc. Format as SRT with timestamps. Include all dialogue and important remarks.
```

## 🎓 Educational Content

### Lecture/Tutorial
```
Transcribe this educational video in SRT format. Pay special attention to technical terms, formulas, and specialized vocabulary. Include all spoken content with accurate timestamps. Preserve the exact wording of key concepts.
```

### Technical Demonstration
```
Transcribe this technical video precisely. Include all spoken instructions, technical terms, code mentions, and command references exactly as spoken. Format as SRT with timestamps. Maintain technical accuracy above all else.
```

### Mathematics/Science
```
Transcribe this video including all mathematical or scientific terminology. Use proper notation when possible (e.g., "x squared" or "x²"). Format as SRT with timestamps. Preserve technical accuracy.
```

## 📺 Entertainment Content

### Movie/TV Show
```
Transcribe this video as movie subtitles. Format in SRT with timestamps. Include dialogue only (no descriptions of sounds or music unless spoken). Use proper punctuation and natural pauses.
```

### Podcast
```
Transcribe this podcast in SRT format. Include all spoken words with timestamps. Preserve the conversational tone and include verbal fillers (um, uh) if significant. Label speakers if multiple people are present.
```

### YouTube Video
```
Transcribe this YouTube video including any important callouts or text mentions by the speaker. Format as SRT with timestamps. Make subtitles easy to read (1-7 seconds per segment).
```

## 🎤 Audio Quality Considerations

### Low Quality Audio
```
Transcribe this video to the best of your ability despite any audio quality issues. Use [inaudible] for parts that cannot be understood. Format as SRT with timestamps. Indicate uncertainty with [?] when needed.
```

### Multiple Languages in One Video
```
Transcribe this multilingual video. Maintain the original language for each segment and indicate language switches like:
[English] Hello everyone
[Spanish] Hola amigos
[English] Let's continue

Format as SRT with timestamps.
```

### Heavy Accent
```
Transcribe this video accurately, interpreting the speaker's accent. Focus on meaning rather than exact pronunciation. Format as SRT with timestamps using standard spelling.
```

## 🎬 Professional Use Cases

### Meeting Transcription
```
Transcribe this meeting recording in SRT format. Include timestamps for all speakers. Capture action items, decisions, and key discussion points. Use [Speaker Name] or [Speaker 1] format.
```

### Webinar
```
Transcribe this webinar including both the presenter's speech and any Q&A portions. Format as SRT with timestamps. Label sections as [Presenter] and [Q&A] where appropriate.
```

### Product Demo
```
Transcribe this product demonstration video. Include all feature explanations, benefits mentioned, and instructions given. Format as SRT with timestamps. Maintain exact product terminology.
```

### Customer Testimonial
```
Transcribe this testimonial video preserving the speaker's exact words and emotion. Format as SRT with timestamps. Keep the authentic voice of the customer.
```

## 📋 Format Variations

### Short Subtitles (Easy Reading)
```
Transcribe this video in SRT format with short, easy-to-read subtitles. Aim for 5-7 words per subtitle, maximum 2 lines. Split long sentences naturally. Include accurate timestamps.
```

### Long Form (More Text Per Subtitle)
```
Transcribe this video in SRT format allowing longer subtitle segments (up to 3 lines or 10-15 seconds). Minimize subtitle breaks to maintain reading flow. Include accurate timestamps.
```

### Word-for-Word
```
Transcribe every single word spoken in this video, including fillers like "um", "uh", "you know", etc. Format as SRT with precise timestamps. Do not summarize or clean up the speech.
```

### Clean Transcription
```
Transcribe this video in SRT format, removing verbal fillers (um, uh, like, you know), false starts, and repetitions. Present the content in clear, readable form while maintaining the original meaning. Include timestamps.
```

## 🎯 Specialized Content

### Music Video with Lyrics
```
Transcribe the lyrics of this music video/song in SRT format with timestamps. Include repeated chorus sections each time they occur. Format for karaoke-style reading if possible.
```

### Documentary
```
Transcribe this documentary including narration and any interviewed subjects. Distinguish between [Narrator] and [Interview Subject] or use names if identifiable. Format as SRT with timestamps.
```

### News Broadcast
```
Transcribe this news segment in SRT format. Include all spoken content by anchors and reporters. Label speakers as [Anchor], [Reporter], [Correspondent] where appropriate. Include timestamps.
```

### Sports Commentary
```
Transcribe this sports commentary including all play-by-play and color commentary. Format as SRT with timestamps. Include excitement and emphasis where natural. Label multiple commentators if present.
```

## 🔧 Custom Template

Use this template to create your own:

```
[What to transcribe]: Transcribe this [type of video]
[Special instructions]: [Include/exclude specific elements]
[Language handling]: [Original language/translate to X]
[Speaker handling]: [Label speakers as X]
[Format requirements]: Format as SRT with timestamps
[Timing]: [Create segments of X seconds]
[Special considerations]: [Preserve/adapt/clean up X]
```

---

## 💡 Tips for Better Prompts

1. **Be Specific**: More detail = better results
2. **Include Format**: Always specify SRT with timestamps
3. **Language Clarity**: State source and target languages clearly
4. **Context Matters**: Mention video type (tutorial, interview, etc.)
5. **Quality Notes**: Mention if audio is poor/accented
6. **Special Needs**: Request speaker labels, technical accuracy, etc.

## 🎚️ Temperature Settings Guide

| Temperature | Best For | Result |
|-------------|----------|--------|
| 0.0 - 0.3   | Technical content, lectures | Very precise, literal |
| 0.4 - 0.7   | General videos, interviews | Balanced accuracy |
| 0.8 - 1.2   | Creative content, marketing | More interpretive |
| 1.3 - 2.0   | Casual content | Very creative (use rarely) |

**Recommendation**: Start with 0.7 for most use cases.

---

Copy and paste these prompts directly into the application's prompt box, modifying as needed for your specific video!
