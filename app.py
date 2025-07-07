import streamlit as st
import validators
import re
import time
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

# -------------------- Helper Functions -------------------- #

def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    """
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

def get_transcript_from_youtube(url):
    """
    Retrieves the full transcript text from a YouTube video.
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Could not extract video ID from the URL.")
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([segment["text"] for segment in transcript])

# -------------------- Streamlit UI -------------------- #

st.set_page_config(page_title="Langchain - Summarize URL Content", page_icon="🦜")
st.title("Langchain: Summarize Content from YouTube or Website")

with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

generic_url = st.text_input("Enter a YouTube or Website URL")

# Prompt Template
prompt_template = """
Provide a summary of the following content in 300 words:
Content: {text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# -------------------- Main Processing -------------------- #

if st.button("Summarize Content"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide both a valid Groq API key and a URL.")
    elif not validators.url(generic_url):
        st.error("The provided URL is not valid.")
    else:
        try:
            llm = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)
            clean_url = generic_url.split('?')[0]  # Remove tracking/query parameters

            with st.spinner("Processing content..."):
                # Load data from YouTube
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    try:
                        transcript_text = get_transcript_from_youtube(clean_url)
                        data = [Document(page_content=transcript_text)]
                    except TranscriptsDisabled:
                        st.error("Transcripts are disabled for this YouTube video.")
                        st.stop()
                    except Exception as e:
                        st.error(f"Failed to fetch transcript: {e}")
                        st.stop()
                # Load data from website
                else:
                    loader = UnstructuredURLLoader(
                        urls=[clean_url],
                        ssl_verify=False,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                                          "Chrome/114.0.0.0 Safari/537.36",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                            "Accept-Language": "en-US,en;q=0.5",
                            "Connection": "keep-alive"
                        }
                    )
                    data = loader.load()

                # Validate content
                if not data or not data[0].page_content.strip():
                    st.error("No content was found to summarize.")
                    st.stop()

                # Split text into chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=100
                )
                docs = text_splitter.split_documents(data)

                # Run summarization using map_reduce
                chain = load_summarize_chain(
                    llm,
                    chain_type="map_reduce",
                    map_prompt=prompt,
                    combine_prompt=prompt
                )
                summary = chain.run(docs)

            # Display summary
            st.subheader("Summary")

            # Typing effect simulation
            placeholder = st.empty()
            typed_text = ""

            for char in summary:
                typed_text += char
                placeholder.markdown(typed_text)
                time.sleep(0.01)  # Typing speed: adjust if needed


        except Exception as e:
            st.exception(f"An error occurred: {e}")
