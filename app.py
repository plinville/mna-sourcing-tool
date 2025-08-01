import streamlit as st
import pandas as pd
from backend.database import CandidateDatabase
from backend.feedback_model import FeedbackModel

# Initialize database and model
db = CandidateDatabase("candidates.db")
model = FeedbackModel()

st.title("M&A Sourcing Tool")
st.write("Review acquisition candidates and provide feedback to improve results.")

# Load unreviewed candidates and convert to DataFrame
candidates_raw = db.get_unreviewed_candidates()
candidates = pd.DataFrame(candidates_raw, columns=["id", "name", "website", "description"])

if candidates.empty:
    st.info("No unreviewed candidates found.")
else:
    selected_index = st.selectbox("Select a candidate to review:", candidates.index, format_func=lambda i: candidates.loc[i, "name"])
    selected = candidates.loc[selected_index]

    st.subheader(selected["name"])
    st.markdown(f"[Visit Website]({selected['website']})")
    st.write(selected["description"])

    feedback_text = st.text_area("Your feedback on this company:", height=150)

    if st.button("Submit Feedback"):
        if feedback_text.strip() == "":
            st.warning("Please enter feedback before submitting.")
        else:
            db.set_feedback(selected["id"], feedback_text)
            st.success("Feedback submitted.")

            ai_response = model.analyze_feedback(feedback_text)
            st.markdown("### AI Interpretation:")
            st.write(ai_response)
