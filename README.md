# Langchain Summarizer: YouTube & Website Content

This Streamlit app uses **Langchain**, **Groq LLMs**, and **YouTubeTranscriptAPI** to summarize content from:

* YouTube videos (via transcript)
* Public website articles

---

## Features

* 🔑 API key input for Groq LLMs
* 🧠 Summarization using Map-Reduce with prompt templates
* 📺 YouTube transcript parsing using `youtube_transcript_api`
* 🌐 Web content extraction using `UnstructuredURLLoader`
* ✂️ Automatic text chunking for long content
* 🖥️ Typing effect display for summary output

---

## How to Use

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/langchain-summarizer.git
   cd langchain-summarizer
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

5. Enter your Groq API key and any valid YouTube or website URL.

---

## Dependencies

* `streamlit`
* `langchain`
* `langchain-groq`
* `langchain-community`
* `youtube-transcript-api`
* `validators`

Install with:

```bash
pip install -r requirements.txt
```

---

## Notes

* Ensure the URL is publicly accessible.
* Some YouTube videos may have transcripts disabled.
* The app uses `map_reduce` summarization for better performance on longer content.

---

## License

MIT

---

## Author

Robin Rawat
