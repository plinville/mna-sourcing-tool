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
        status = st.radio("Status:", ["approved", "rejected", "unsure"])

        if st.button("Submit Feedback"):
            if feedback_text.strip():
                result = model.analyze_feedback(feedback_text)

                if not isinstance(result, dict) or "content" not in result:
                    st.error("⚠️ Unexpected response from feedback model.")
                else:
                    analysis = result["content"]
                    db.update_feedback(candidate['id'], analysis, status)
                    st.success(f"Feedback saved with status: {status}.")
                    st.rerun()
            else:
                st.warning("Please provide feedback text before submitting.")

    # Step 3: Display approved candidates
    st.divider()
    st.subheader("✅ Approved Candidates")
    approved_df = db.get_approved_candidates()
    if not approved_df.empty:
        st.dataframe(approved_df[["name", "website", "summary"]])
    else:
        st.write("No approved candidates yet.")

    # Optional: Full database view (for debugging)
    with st.expander("📊 Debug: All candidates in DB"):
        st.dataframe(db.get_all_candidates())
