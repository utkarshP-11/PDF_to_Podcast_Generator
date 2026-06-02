import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from pydub import AudioSegment
import pymupdf4llm
import asyncio
import edge_tts
import tempfile
import os
import nest_asyncio
import time
from datetime import timedelta

load_dotenv()
nest_asyncio.apply()

st.set_page_config(page_title="Advanced PDF to Podcast", layout="wide")

st.title("🎙️ Advanced PDF to Podcast Generator")

if "generated" not in st.session_state:
    st.session_state.generated = False
if "script" not in st.session_state:
    st.session_state.script = ""
if "audio_path" not in st.session_state:
    st.session_state.audio_path = ""
if "timestamps" not in st.session_state:
    st.session_state.timestamps = []
if "extraction_time" not in st.session_state:
    st.session_state.extraction_time = 0.0
if "script_time" not in st.session_state:
    st.session_state.script_time = 0.0
if "audio_time" not in st.session_state:
    st.session_state.audio_time = 0.0
if "total_runtime" not in st.session_state:
    st.session_state.total_runtime = 0.0
if "chunks_count" not in st.session_state:
    st.session_state.chunks_count = 0
if "words_count" not in st.session_state:
    st.session_state.words_count = 0
if "estimated_tokens" not in st.session_state:
    st.session_state.estimated_tokens = 0
if "words_per_second" not in st.session_state:
    st.session_state.words_per_second = 0.0
if "srt_content" not in st.session_state:
    st.session_state.srt_content = ""
if "generate_transcript" not in st.session_state:
    st.session_state.generate_transcript = False
if "generate_srt" not in st.session_state:
    st.session_state.generate_srt = False

# api_key = os.getenv("GROQ_API_KEY") or 
api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

podcast_style = st.selectbox(
    "Podcast Style",
    ["Educational", "Casual", "Technical Deep Dive", "News Debate", "Storytelling", "Interview", "Beginner Friendly"]
)

podcast_duration = st.selectbox("Podcast Length", ["5 minutes", "15 minutes", "30 minutes"])
language = st.selectbox("Language", ["English", "Hindi"])

voice_1 = st.selectbox("Host 1 Voice", ["en-US-ChristopherNeural", "en-GB-RyanNeural", "hi-IN-MadhurNeural"])
voice_2 = st.selectbox("Host 2 Voice", ["en-US-JennyNeural", "en-GB-SoniaNeural", "hi-IN-SwaraNeural"])

enable_music = st.checkbox("Add Background Music")
generate_transcript_opt = st.checkbox("Generate Transcript")
generate_srt_opt = st.checkbox("Generate Subtitle File (.srt)")

@st.cache_resource
def load_llm(api_key):
    return ChatGroq(temperature=0.7, model_name="llama-3.3-70b-versatile", groq_api_key=api_key)

@st.cache_data
def extract_pdf_text(pdf_path):
    return pymupdf4llm.to_markdown(pdf_path)

def create_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=500)
    return splitter.split_text(text)

def create_prompt(style, duration, language):
    return f"""
    You are generating a high-quality podcast between two hosts.\n\n
    Podcast Style:\n{style}\n\n
    Target Length:\n{duration}\n\n
    Language:\n{language}\n\n
    Rules:\n- 
    Sound natural\n- 
    Add curiosity and reactions\n- 
    Explain concepts clearly\n- 
    Use conversational transitions\n- 
    Add occasional humor\n- 
    Avoid robotic dialogue\n- 
    Add emotional expressions\n- 
    Keep audience engaged\n\n
    Format STRICTLY:
    \nHost 1: ...\nHost 2: ...\n\n
    DO NOT break the format."""

async def generate_audio_segment(text, voice, filename):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(filename)

def format_timestamp(seconds):
    return str(timedelta(seconds=int(seconds)))

if st.button("Generate Podcast"):
    if not uploaded_file:
        st.error("Please upload a PDF.")
        st.stop()
    if not api_key:
        st.error("Please provide API key.")
        st.stop()

    total_start = time.time()
    st.session_state.generate_transcript = generate_transcript_opt
    st.session_state.generate_srt = generate_srt_opt

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(uploaded_file.read())
            pdf_path = tmp_pdf.name

        st.info("Extracting PDF text...")
        extraction_start = time.time()
        document_text = extract_pdf_text(pdf_path)
        st.session_state.extraction_time = round(time.time() - extraction_start, 2)

        if not document_text.strip():
            st.error("No readable text found in PDF.")
            st.stop()

        st.info("Chunking document...")
        chunks = create_chunks(document_text)
        st.session_state.chunks_count = len(chunks)
        llm = load_llm(api_key)

        st.info("Generating chunk summaries...")
        chunk_summaries = []
        summary_prompt = PromptTemplate.from_template("Summarize this chunk clearly for podcast generation.\n\nChunk:\n{text}")
        summary_chain = summary_prompt | llm | StrOutputParser()

        for idx, chunk in enumerate(chunks):
            with st.spinner(f"Processing chunk {idx+1}/{len(chunks)}"):
                summary = summary_chain.invoke({"text": chunk})
                chunk_summaries.append(summary)

        combined_summary = "\n".join(chunk_summaries)
        st.info("Generating podcast script...")
        script_start = time.time()
        final_prompt = PromptTemplate.from_template("{instructions}\n\nContent:\n{text}")
        chain = final_prompt | llm | StrOutputParser()
        
        script = chain.invoke({
            "instructions": create_prompt(podcast_style, podcast_duration, language),
            "text": combined_summary
        })
        
        st.session_state.script = script
        st.session_state.script_time = round(time.time() - script_start, 2)
        lines = script.split("\n")

        st.info("Generating audio...")
        audio_start = time.time()
        temp_files = []
        tasks = []
        timestamp_data = []
        current_time = 0

        for idx, line in enumerate(lines):
            if line.startswith("Host 1:"):
                text = line.replace("Host 1:", "").strip()
                voice = voice_1
            elif line.startswith("Host 2:"):
                text = line.replace("Host 2:", "").strip()
                voice = voice_2
            else:
                continue

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_file.close()
            temp_files.append(temp_file.name)
            
            timestamp_data.append({
                "time": current_time,
                "text": text[:80]
            })
            
            estimated_duration = max(len(text.split()) / 2.5, 2)
            current_time += estimated_duration
            tasks.append(generate_audio_segment(text, voice, temp_file.name))

        asyncio.run(asyncio.gather(*tasks))
        combined_audio = AudioSegment.empty()

        for file in temp_files:
            audio = AudioSegment.from_mp3(file)
            combined_audio += audio

        if enable_music and os.path.exists("background_music.mp3"):
            bg_music = AudioSegment.from_mp3("background_music.mp3")
            bg_music = bg_music - 25
            bg_music = bg_music[:len(combined_audio)]
            combined_audio = combined_audio.overlay(bg_music)

        final_audio_path = "final_podcast.mp3"
        combined_audio.export(final_audio_path, format="mp3")

        for file in temp_files:
            os.remove(file)

        st.session_state.audio_time = round(time.time() - audio_start, 2)
        st.session_state.timestamps = timestamp_data
        st.session_state.audio_path = final_audio_path
        st.session_state.total_runtime = round(time.time() - total_start, 2)

        words = len(script.split())
        st.session_state.words_count = words
        st.session_state.estimated_tokens = int(words * 1.3)
        st.session_state.words_per_second = round(words / st.session_state.total_runtime, 2)

        if st.session_state.generate_srt:
            srt_content = ""
            for idx, item in enumerate(timestamp_data):
                start = format_timestamp(item["time"])
                end = format_timestamp(item["time"] + 5)
                srt_content += f"{idx+1}\n{start},000 --> {end},000\n{item['text']}\n\n"
            st.session_state.srt_content = srt_content

        st.session_state.generated = True
        st.rerun()

    except Exception as e:
        st.error(f"Error: {str(e)}")

if st.session_state.generated:
    st.success("Podcast Generated Successfully!")
    
    st.subheader("📜 Generated Script")
    st.write(st.session_state.script)

    st.subheader("🎧 Podcast Audio")
    if os.path.exists(st.session_state.audio_path):
        st.audio(st.session_state.audio_path)
        with open(st.session_state.audio_path, "rb") as f:
            st.download_button("Download Podcast", data=f, file_name="podcast.mp3", mime="audio/mpeg")

    if st.session_state.generate_transcript:
        st.download_button("Download Transcript", data=st.session_state.script, file_name="transcript.txt", mime="text/plain")

    if st.session_state.generate_srt and st.session_state.srt_content:
        st.download_button("Download Subtitles", data=st.session_state.srt_content, file_name="podcast.srt", mime="text/plain")

    st.subheader("Podcast Timeline")
    for item in st.session_state.timestamps:
        st.write(f"{format_timestamp(item['time'])} - {item['text']}")

    st.subheader("Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("PDF Extraction", f"{st.session_state.extraction_time}s")
    col2.metric("Script Generation", f"{st.session_state.script_time}s")
    col3.metric("Audio Generation", f"{st.session_state.audio_time}s")
    col4.metric("Total Runtime", f"{st.session_state.total_runtime}s")

    st.subheader(" System Metrics")
    st.write(f"AI Text Chunks Created for Processing: {len(chunks)}")
    st.write(f"Total Words in Generated Podcast Script: {st.session_state.words_count}")
    st.write(f"Estimated LLM Tokens Used: {st.session_state.estimated_tokens}")
    st.write(f"Podcast Generation Speed in Words Per Second: {st.session_state.words_per_second}")