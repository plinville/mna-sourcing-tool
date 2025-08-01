import streamlit as st
import pandas as pd
import os
import shutil
from datetime import datetime

from backend.database import CandidateDatabase
from backend.feedback_model import FeedbackModel
from backend.scraper import search_and_store_candidates

DB_PATH = "candidates_v2.db"
db = CandidateDatabase(DB_PATH)
model = FeedbackModel()

st.title("🤝 M&A Acquisition Candidate Evaluator")

# Sidebar: Reset DB with backup and confirmation
st.sidebar.header("Admin")

if st.sidebar.button("🗑️ Reset Candidate Database"):
    confirm = st.sidebar.radio("Are you sure?", ["No", "Yes, reset"])
    if confirm == "Yes, reset":
        if os.path.exists(DB_PATH):
            # Backup first
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_candidates_{timestamp}.db"
            shutil.copy(DB_PATH, backup_name)
            os.remove(DB_PATH)
            st.sidebar.success(f"✅ DB reset. Backup saved as {backup_name}")
            st.stop()
        else:
            st.sidebar.warning("No existing database to reset.")

# Export all candidates
if st.sidebar.button("📤 Export All Feedback to CSV"):
    try:
        all_df = db.get_all_candidates()
        csv = all_df.to_csv(index=False)
        st.sidebar.download_button("Download CSV", data=csv, file_name="all_candidates.csv", mime="text/csv")
    except Exception as e:
        st.sidebar.error(f"❌ Export failed: {e}")

# Session state
if "keywords_submitted" not in st.session_state:
    st.session_state.keywords_submitted = False
    st.session_state.keywords = ""

# Search UI
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
    candidates = db.get_unreviewed_candidates()

    if candidates.empty:
        st.info("✅ No unreviewed candidates found.")
    else:
        candidate = candidates.iloc[0]
        st.subheader("Review Candidate")
        st.write(f"**Name:** {candidate['name']}")
        st.write(f"**Website:** {candidate['website']}")
        st.write(f"**Summary:** {candidate['summary']}")

        feedback_text = st.text_area("🧠 Why is this company a good or bad fit?")
        status = st.radio("Status", ["approved", "rejected", "unsure"])

        if st.button("Submit Feedback"):
            if feedback_text.strip():
                try:
                    result = model.analyze_feedback(feedback_text)

                    if not isinstance(result, dict) or "content" not in result:
                        st.error("⚠️ Unexpected response from feedback model.")
                    else:
                        analysis = result["content"]
                        db.update_feedback(candidate["id"], analysis, status)
                        st.success(f"✅ Feedback saved. Status: {status}.")
                        st.rerun()
                except Exception as e:
                    st.error(f"⚠️ AI feedback failed: {str(e)}")
            else:
                st.warning("Please provide feedback text before submitting.")

    # Approved list
    st.divider()
    st.subheader("✅ Approved Candidates")
    try:
        approved_df = db.get_approved_candidates()
        if not approved_df.empty:
            st.dataframe(approved_df[["name", "website", "summary"]])
        else:
            st.write("No approved candidates yet.")
    except Exception as e:
        st.error(f"❌ Error loading approved candidates: {e}")

    # Debug
    with st.expander("📊 Debug: All candidates"):
        try:
            all_df = db.get_all_candidates()
            st.dataframe(all_df)
        except Exception as e:
            st.write("Error loading all candidates:", e)
