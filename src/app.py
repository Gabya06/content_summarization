import streamlit as st
import pandas as pd
import os

from dotenv import load_dotenv
from google import genai

from summarize import ContentSummary


st.set_page_config(page_title="AI Model Comparison", layout="wide")
st.title(":star: AI Transformer Model Comparison")
st.subheader(":punch: BART vs T5-Large Summarization using Google Gemini")


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

st.sidebar.header("Upload Data")
bart_file = st.sidebar.file_uploader("Upload BART CSV", type="csv")
t5_file = st.sidebar.file_uploader("Upload T5-Large CSV", type="csv")

if bart_file and t5_file:
    bart_data = pd.read_csv(bart_file, index_col=0)
    t5_data = pd.read_csv(t5_file, index_col=0)
    data = bart_data.merge(t5_data, on="title", suffixes=["_bart", "_t5"])
    data = data[
        [
            "title",
            "cleaned_text_bart",
            "summary_bart",
            "summary_t5",
            "sentiment_bart",
            "num_comments_bart",
        ]
    ]
    data.rename(
        columns={
            "cleaned_text_bart": "cleaned_text",
            "sentiment_bart": "sentiment",
            "num_comments_bart": "num_comments",
        },
        inplace=True,
    )
    data = data[
        [
            "title",
            "sentiment",
            "num_comments",
            "cleaned_text",
            "summary_bart",
            "summary_t5",
        ]
    ]
    st.write("### Sample Data")
    st.dataframe(data.head(), use_container_width=True, hide_index=True)

    sample_size = st.slider(
        "Number of posts to summarize",
        min_value=1,
        max_value=min(20, len(data)),
        value=5,
    )
    sample_rows = data.head(sample_size).to_dict(orient="records")

    if st.button("Summarize and Compare"):
        with st.spinner("Generating summaries..."):
            summaries = ContentSummary.summarize_rows(client, sample_rows)
        max_comments = (
            max(row["num_comments"] for row in sample_rows) or 1
        )  # avoid division by zero

        # Sentiment to emoji mapping
        sentiment_emoji = {"positive": "😊", "neutral": "😐", "negative": "😞"}

        for i, (row, summary) in enumerate(zip(sample_rows, summaries), 1):
            with st.expander(f"Post {i}: {row['title']}"):
                col1, col2 = st.columns([1, 4])
                with col1:
                    emoji = sentiment_emoji.get(str(row["sentiment"]).lower(), "❓")
                    st.markdown(
                        f"<span style='font-size:1.5em'>{emoji}</span><br>"
                        f"<span style='font-size:0.8em'>{row['sentiment'].capitalize()}</span>",
                        unsafe_allow_html=True,
                    )

                with col2:
                    st.markdown("**Number of Comments**")
                    st.progress(
                        int(row["num_comments"]) / max_comments,
                        text=f"{row['num_comments']} comments",
                    )

                st.markdown("**Original Post:**")
                st.code(row["cleaned_text"], language="markdown")

                st.markdown("**BART Summary:**")
                st.code(row["summary_bart"], language="markdown")

                st.markdown("**T5-Large Summary:**")
                st.code(row["summary_t5"], language="markdown")
                st.markdown("---")
                st.markdown(f"**Gemini Summary & Comparison:**\n\n{summary}")
else:
    st.info("Please upload both BART and T5-Large CSV files to begin.")
