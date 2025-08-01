import streamlit as st
import pandas as pd
from backend.database import CandidateDatabase
from backend.feedback_model import FeedbackModel
from backend.scraper import search_and_store_candidates

# Load database and feedback model
db = CandidateDatabase("candidates_v2.db")
model = FeedbackModel()

st.title("🤝 M&A Acquisition Candidate Evaluator")

# Initialize session state
if "keywords_submitted" not in st.session_state:
    st.session_state.keywords_submitted = False
    st.session_state.keywords = ""

# Step 1: Get keywords from user
if not st.session_state.keywords_submitted:
    st.subheader("Start a New Search")
    st.session_state.keywords = st.text_input("Enter keywords (e.g., pediatric therapy, adolescent therapy):")

    if st.button("Search"):
        if st.session_state.keywords.strip():
            search_and_store_candidates(st.session_state.keywords, db, limit=5)
            st.session_state.keywords_submitted = True
            st.rerun()
        else:
            st.warning("Please enter keywords to begin.")
else:
    # Step 2: Review candidates
    candidates = db.get_unreviewed_candidates()
    if candidates.empty:
        st.info("✅ No unreviewed candidates found.")
    else:
        candidate = candidates.iloc[0]
        st.subheader("Review Candidate")
        st.write(f"**Name:** {candidate['name']}")
        st.write(f"**Website:** {candidate['website']}")
        st.write(f"**Summary:** {candidate['summary']}")

        feedback_text = st.text_area("Why is this company a good or bad fit?")

        if st.button("Submit Feedback"):
            if feedback_text.strip():
                result = model.analyze_feedback(feedback_text)
                analysis = result["content"]
                model_used = result["model_used"]

                if model_used == "error":
                    st.error(f"⚠️ AI feedback failed: {analysis}")
                elif model_used == "gpt-3.5-turbo":
                    st.warning("⚠️ GPT-4o was unavailable — response generated using GPT-3.5.")
                    st.write("📝 GPT Feedback:", analysis)
                    db.update_feedback(candidate['id'], analysis)
                    st.success("Feedback submitted and saved.")
                    st.rerun()
                else:
                    st.write("📝 GPT Feedback:", analysis)
                    db.update_feedback(candidate['id'], analysis)
                    st.success("Feedback submitted and saved.")
                    st.rerun()
            else:
                st.warning("Please write some feedback before submitting.")

    # Debug: Show full table
    st.divider()
    st.subheader("📊 Debug: All candidates in DB")
    st.dataframe(pd.read_sql_query("SELECT * FROM candidates", db.conn))
