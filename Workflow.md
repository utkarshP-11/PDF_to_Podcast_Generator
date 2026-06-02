# 🔄 PDF to Podcast Generator — System Workflow

---

# 🏗️ Complete System Architecture

```text
                                                        ┌──────────────────────┐
                                                        │   User Uploads PDF   │
                                                        └──────────┬───────────┘
                                                                   │
                                                                   ▼
                                                        ┌──────────────────────┐
                                                        │ Streamlit Frontend UI│
                                                        │  - Upload PDF        │
                                                        │  - Select Style      │
                                                        │  - Choose Voices     │
                                                        │  - Select Language   │
                                                        └──────────┬───────────┘
                                                                   │
                                                                   ▼
                                                        ┌──────────────────────┐
                                                        │ PDF Validation Layer │
                                                        │ - Check API Key      │
                                                        │ - Validate PDF       │
                                                        │ - Error Handling     │
                                                        └──────────┬───────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ PDF Text Extraction Engine │
                                                        │     PyMuPDF4LLM            │
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ Extracted Raw Document Text│
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ Recursive Text Chunking    │
                                                        │ chunk_size = 4000          │
                                                        │ overlap = 500              │
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                             ┌───────────────┐
                                                             │ Text Chunks   │
                                                             └──────┬────────┘
                                                                    │
                                                                    ▼
                                                        ┌────────────────────────────┐
                                                        │ Chunk Summarization Layer  │
                                                        │     LangChain + Groq       │
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ Combined Summarized Context│
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ Podcast Prompt Engineering │
                                                        │ - Style                    │
                                                        │ - Duration                 │
                                                        │ - Language                 │
                                                        │ - Conversational Rules     │
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ AI Podcast Script Generator│
                                                        │   llama-3.3-70b-versatile  │
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ Generated Podcast Script   │
                                                        │ Host 1                     │
                                                        │ Host 2                     │
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ Script Line Processing     │
                                                        │ Voice Assignment           │
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ Async Edge-TTS Generation  │
                                                        │ Parallel Audio Synthesis   │
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ Temporary MP3 Segments     │
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ Audio Merging Pipeline     │
                                                        │        Pydub + FFmpeg      │
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ Background Music Overlay   │
                                                        │      (Optional)            │
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ Final Podcast MP3 Export   │
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ Transcript & Subtitle Gen  │
                                                        │ - TXT Transcript           │
                                                        │ - SRT Subtitle File        │
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ Performance Metrics Engine │
                                                        │ - Runtime                  │
                                                        │ - Token Estimate           │
                                                        │ - Chunk Count              │
                                                        │ - Processing Speed         │
                                                        └──────────┬─────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌────────────────────────────┐
                                                        │ Final Streamlit Output UI  │
                                                        │ - Audio Player             │
                                                        │ - Downloads                │
                                                        │ - Metrics Dashboard        │
                                                        └────────────────────────────┘
```

---

# 🧠 Detailed AI Processing Flow

```text
PDF
 │
 ▼
Extract Text
 │
 ▼
Split into Chunks
 │
 ├── Chunk 1 ──► Summarize
 ├── Chunk 2 ──► Summarize
 ├── Chunk 3 ──► Summarize
 │
 ▼
Merge Summaries
 │
 ▼
Generate Conversational Podcast
 │
 ▼
Host-Based Dialogue Output
```

---

# 🎧 Audio Generation Workflow

```text
Podcast Script
      │
      ▼
Line-by-Line Parsing
      │
      ├── Host 1 → Voice A
      ├── Host 2 → Voice B
      │
      ▼
Edge-TTS Async Generation
      │
      ▼
Temporary Audio Files
      │
      ▼
Pydub Audio Merge
      │
      ▼
FFmpeg MP3 Export
      │
      ▼
Final Podcast Audio
```

---

# ⚡ Performance Optimization Workflow

```text
Large PDF
    │
    ▼
Chunk Processing
    │
    ▼
Parallel TTS Generation
    │
    ▼
Reduced Runtime
```

### Optimizations Used

* Async audio generation
* Cached model loading
* Cached PDF extraction
* Chunked LLM processing
* Parallel TTS synthesis

---

# 📊 Metrics Collection Pipeline

```text
PDF Extraction Time
        +
Chunk Processing Time
        +
LLM Generation Time
        +
Audio Synthesis Time
        +
Export Time
        ↓
Total Runtime
```

---

# 🛡️ Error Handling Workflow

```text
User Action
     │
     ▼
Validation Checks
     │
     ├── Missing PDF
     ├── Invalid API Key
     ├── Empty PDF
     ├── FFmpeg Missing
     ├── Audio Export Failure
     │
     ▼
Graceful Error Messages
```

---

# 🌍 Multi-Language Support Pipeline

```text
Selected Language
       │
       ▼
Prompt Customization
       │
       ▼
Language-Specific Script
       │
       ▼
Voice Model Selection
       │
       ▼
Localized Podcast Audio
```

---

# 📁 Output Generation Flow

```text
Generated Script
      │
      ├── MP3 Podcast
      ├── TXT Transcript
      ├── SRT Subtitles
      │
      ▼
Downloadable Assets
```

---

# 🚀 Final System Overview

```text
PDF + AI + TTS + Audio Processing
                ↓
      Fully Generated Podcast
```
