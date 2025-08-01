import streamlit as st
from scraper import scrape_candidates
from backend.database import CandidateDatabase
from backend.feedback_model import FeedbackModel

st.title("M&A Sourcing Assistant")

st.sidebar.header("Search Parameters")
keywords = st.sidebar.text_input("Keywords", "pediatric therapy, adolescent therapy")
num_results = st.sidebar.slider("Number of results", 5, 50, 10)

if "feedback_model" not in st.session_state:
    st.session_state.feedback_model = FeedbackModel()
if "db" not in st.session_state:
    st.session_state.db = CandidateDatabase("data/candidates.db")

if st.sidebar.button("Run Search"):
    candidates = scrape_candidates(keywords, num_results)
    for c in candidates:
        st.session_state.db.insert_candidate(c)
    st.experimental_rerun()

st.subheader("Review Candidates")
candidates = st.session_state.db.get_unreviewed()
if not candidates:
    st.info("No unreviewed candidates found.")
else:
    for c in candidates:
        with st.expander(c['name']):
            st.markdown(f"**URL**: [{c['url']}]({c['url']})")
            st.markdown(f"**Snippet**: {c['snippet']}")
            feedback = st.radio("Feedback", ["Good Fit", "Maybe", "Not a Fit"], key=c['url'])
            reason = st.text_area("Reason for your feedback", key=c['url']+"_reason")
            if st.button("Submit Feedback", key=c['url']+"_submit"):
                st.session_state.db.update_feedback(c['url'], feedback, reason)
                st.session_state.feedback_model.add_feedback(c['snippet'], feedback)
                st.success("Feedback submitted.")
                st.experimental_rerun()
