import streamlit as st
from backend.database import CandidateDatabase
from backend.feedback_model import FeedbackModel
import os

st.title("M&A Acquisition Candidate Evaluator")

# Initialize database and model
db = CandidateDatabase()
model = FeedbackModel()

# Step 1: Get keyword input from the user
if "keywords_submitted" not in st.session_state:
    st.session_state.keywords_submitted = False
    st.session_state.keywords = ""

if not st.session_state.keywords_submitted:
    st.subheader("Start a New Search")
    st.session_state.keywords = st.text_input("Enter keywords (e.g., pediatric therapy, adolescent therapy):")
    if st.button("Search"):
        if st.session_state.keywords.strip():
            # Run the scraper for 5 results using provided keywords
            from backend.scraper import search_and_store_candidates
            search_and_store_candidates(st.session_state.keywords, num_results=5)
            st.session_state.keywords_submitted = True
            st.experimental_rerun()
        else:
            st.warning("Please enter some keywords to start the search.")

# Step 2: Show unreviewed candidates one at a time
else:
    candidates = db.get_unreviewed_candidates()
    if candidates.empty:
        st.info("No unreviewed candidates found.")
    else:
        candidate = candidates.iloc[0]
        st.subheader("Review Candidate")
        st.write(f"**Name:** {candidate['name']}")
        st.write(f"**Website:** {candidate['website']}")
        st.write(f"**Description:** {candidate['description']}")
        st.write(f"**Relevance Score:** {candidate['score']:.4f}")

        feedback_text = st.text_area("Why is this company a good or bad fit?")

        if st.button("Submit Feedback"):
            if feedback_text.strip():
                analysis = model.analyze_feedback(feedback_text)
                db.save_feedback(candidate['id'], analysis)
                st.success("Feedback submitted and candidate updated.")
                st.experimental_rerun()
            else:
                st.warning("Please provide feedback before submitting.")
