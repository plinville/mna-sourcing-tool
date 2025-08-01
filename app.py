import streamlit as st
import pandas as pd
from backend.database import CandidateDatabase
from backend.feedback_model import FeedbackModel

# Initialize database and feedback model
db = CandidateDatabase("candidates.db")
model = FeedbackModel()

st.set_page_config(page_title="M&A Sourcing Tool", layout="wide")
st.title("M&A Acquisition Candidate Review")

# Load unreviewed candidates
candidates = db.get_unreviewed_candidates()

if candidates.empty:
    st.info("No unreviewed candidates found.")
else:
    index = st.number_input("Candidate index", min_value=0, max_value=len(candidates)-1, step=1)
    row = candidates.iloc[index]

    st.subheader(f"Candidate: {row['name']}")
    st.write(f"**Website:** [{row['url']}]({row['url']})")
    st.write(f"**Description:** {row['description']}")
    st.write(f"**Relevance Score:** {row['score']:.2f}")

    feedback = st.radio("Is this a good fit?", ["Unreviewed", "Yes", "Maybe", "No"])

    custom_comment = st.text_area("Add comments or reasoning here (optional):", height=150)

    if st.button("Submit Feedback"):
        if feedback == "Unreviewed":
            st.warning("Please select a feedback option.")
        else:
            ai_summary = model.analyze(custom_comment) if custom_comment.strip() else ""
            db.update_feedback(
                candidate_id=row["id"],
                feedback=feedback,
                comments=custom_comment,
                ai_summary=ai_summary
            )
            st.success("Feedback submitted!")
            st.experimental_rerun()

# Optional: show full table in expandable section
with st.expander("See all unreviewed candidates"):
    st.dataframe(candidates.drop(columns=["id"]))
