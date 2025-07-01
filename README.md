# AI Transformer Model Comparison: Reddit Post Summarization

This is an **AI-powered Streamlit app** for summarizing Reddit posts and comparing the outputs of two transformer models: **BART** and **T5-Large**. It uses Google Gemini to generate a concise summary and highlight differences between the model-generated summaries. 

* To learn more about the Hugging Face pipeline, `BART` and `T5-Large` transfomer models, you can follow along on [Medium.com](https://medium.com/@gabya06/t5-vs-bart-the-battle-of-the-summarization-models-c1e6d37e56ca).

* The Reddit API was used to generate the data for this repo; you can read about it [here](https://medium.com/@gabya06/automating-reddit-summaries-pulling-data-with-python-91afeb6acdb3).

---

## Features

- **Upload CSVs** with `BART` and `T5-Large` summaries for Reddit posts
- **AI-generated summary & comparison** using Google Gemini
- **Visualize sentiment** (with emoji) and number of comments (progress bar)
- **Interactive UI** built with Streamlit
- **Batch processing** of multiple posts
- **Docker-ready** for easy deployment

---

## Project Structure

```
content_summarization/
│
├── app.py                  # Streamlit app entry point
├── summarize.py            # Summarization logic and ContentSummary class
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker build instructions
├── .env.example            # Example environment variables
├── README.md               # Project documentation
│
├── data/                   # Sample data
│
└── tests/                  # (TODO) Unit tests
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/gabya06/content_summarization.git
cd content_summarization
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Copy `.env.example` to `.env` and add your [Google Gemini API key](https://aistudio.google.com/app/apikey):

```
GEMINI_API_KEY=your-key-here
```

---

## Usage

### Run locally

```bash
streamlit run app.py
```

- Upload your BART and T5-Large CSV files in the sidebar.
- Select the number of posts to summarize.
- Click **Summarize and Compare** to view results.

### CSV Format

Your CSVs should have at least these columns:

- `title`
- `cleaned_text`
- `summary_bart` (for BART CSV)
- `summary_t5` (for T5-Large CSV)
- `sentiment`
- `num_comments`

---

## Docker Deployment

### Build and run with Docker

```bash
docker build -t content-summarization .
docker run -p 8501:8501 --env-file .env content-summarization
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---
## Google Cloud 
Check out the app in [Google Cloud!](https://content-summarization-app-61465655650.us-east1.run.app)
## Customization

- Edit `summarize.py` to change prompt logic or add more models.
- Tweak `app.py` for UI changes or new visualizations.

---

## Acknowledgements

- [Google Gemini](https://aistudio.google.com/)
- [Streamlit](https://streamlit.io/)
- [Hugging Face Transformers](https://huggingface.co/transformers/)

---

