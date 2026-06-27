# PDF to Podcast Generator

This is a Streamlit-based an advanced AI-powered application that converts PDF documents into engaging multi-speaker podcast conversations
using Large Language Models and Text-to-Speech synthesis.

Built using:

* Streamlit
* LangChain
* Groq LLM
* Edge TTS
* PyMuPDF
* Pydub
* FFmpeg

---
#  System Workflow

```text
PDF Upload
    ↓
PDF Text Extraction
    ↓
Chunk Splitting
    ↓
Chunk Summarization
    ↓
Podcast Script Generation
    ↓
Multi-Speaker TTS
    ↓
Audio Merging
    ↓
Final Podcast Export
```

---

#  Features

## Smart PDF Processing

* Extracts text from PDFs using `PyMuPDF4LLM`
* Handles large documents efficiently
* Splits long content into AI-processable chunks

---

##  AI Podcast Script Generation

* Uses Groq LLM (`llama-3.3-70b-versatile`)
* Generates natural 2-host podcast conversations
* Supports multiple podcast styles:

  * Educational
  * Casual
  * Technical Deep Dive
  * News Debate
  * Storytelling
  * Interview
  * Beginner Friendly

---

##  Realistic Multi-Speaker Audio

* Converts script into realistic speech using Edge TTS
* Supports multiple voices and accents
* Async parallel audio generation for faster performance

---

##  Multi-Language Support

Supports:

* English
* Hindi

---

##  Background Music Support

Optional background music overlay for more immersive podcasts.

---

##  Transcript & Subtitle Export

Generate:

* Podcast transcript (`.txt`)
* Subtitle file (`.srt`)
* Final podcast audio (`.mp3`)

---

##  Performance Metrics Dashboard

Tracks:

* PDF extraction time
* AI script generation time
* Audio generation time
* Total runtime
* Estimated token usage
* AI chunk count
* Generation speed

---

#  Tech Stack

| Technology                     | Purpose             |
| ------------------------------ | ------------------- |
| Streamlit                      | Frontend UI         |
| LangChain                      | LLM orchestration   |
| Groq API                       | Fast LLM inference  |
| Edge TTS                       | Speech synthesis    |
| PyMuPDF4LLM                    | PDF extraction      |
| RecursiveCharacterTextSplitter | Chunking large PDFs |
| Pydub                          | Audio merging       |
| FFmpeg                         | Audio processing    |

---

#  Installation

## 1. Clone Repository

```bash
git clone https://github.com/utkarshP-11/pdf-to-podcast-generator.git
cd pdf-to-podcast-generator
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 4. Install FFmpeg

FFmpeg is required for audio processing.

### Windows

```bash
winget install ffmpeg
```

Verify installation:

```bash
ffmpeg -version
```

---

#  Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_api_key_here
```

Get API key from:

https://console.groq.com/keys

---

#  Run Application

```bash
streamlit run app.py
```

---

#  Project Structure

<!---```bash
pdf-to-podcast-generator/
│
├── app.py
├── requirements.txt
├── .env
├── final_podcast.mp3
├── transcript.txt
├── podcast.srt
├── background_music.mp3
└── README.md-->
```bash
PDF_to_Podcast_Generator/
├── .gitignore          # standard git exclusion file
├── README.md           # project overview, tech stack, and installation guides
├── Workflow.md         # detailed architectural diagrams and process flows
├── app.py              # main application logic, Streamlit UI, and orchestration
└── requirements.txt    # python dependencies (langchain, groq, edge-tts, etc.)
```

---

#  Performance Optimizations

Implemented:

* Async audio generation
* Chunk-based processing
* Cached LLM loading
* Cached PDF extraction
* Parallel TTS synthesis

---

#  Current Limitations

* Scanned PDFs may require OCR support
* Very large PDFs can increase runtime
* Background music file must be manually provided
* Podcast duration is approximate

---

#  Future Improvements

Planned upgrades:

* RAG-based retrieval pipeline
* Interactive podcast editing
* Streaming audio generation
* Cloud deployment
* User authentication
* Podcast chapter generation
* Emotion-aware TTS
* YouTube-ready exports
* Podcast memory across chunks

---

#  Demo Features

* Upload PDF  
* Select podcast style  
* Choose voices  
* Generate podcast  
* Download audio  
* Export transcript  
* Export subtitles  
* View performance metrics  
  
---

#  Contributing

Contributions are welcome.

Steps:

1. Fork repository
2. Create feature branch
3. Commit changes
4. Open pull request

