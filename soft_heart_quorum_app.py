
import streamlit as st
import random

# --- Session Initialization ---
if 'group' not in st.session_state:
    st.session_state.group = random.choice(['Group 1', 'Group 2', 'Group 3', 'Group 4'])
if 'submitted_resolutions' not in st.session_state:
    st.session_state.submitted_resolutions = {}
if 'scores' not in st.session_state:
    st.session_state.scores = {}

# --- Title and Group Info ---
st.title("🧡 Soften Your Heart - Quorum Activity")
st.subheader(f"You are in **{st.session_state.group}**")

# --- Soft Heart Assessment ---
st.header("Step 1: Heart Softness Assessment")
questions = [
    "Do I sincerely repent each day?",
    "Do I study the scriptures regularly?",
    "Do I pray with intent and listen?",
    "Do I submit my will to God's?",
    "Do I forgive those who hurt me?",
    "Do I serve even when it's inconvenient?",
    "Do I share my testimony regularly?",
    "Do I follow prophetic counsel?",
    "Am I open to correction or redirection?",
    "Do I recognize and follow spiritual promptings?"
]
score = 0
for q in questions:
    score += st.slider(q, 0, 3, key=q)
st.markdown(f"### 💬 Your Score: **{score}/30**")
if score >= 25:
    st.success("Your heart is soft and open to the Spirit.")
elif score >= 18:
    st.warning("You're on the path — keep softening your heart daily.")
else:
    st.error("Time to return to the Lord with full purpose of heart.")

# --- Scenario Section ---
st.header("Step 2: Your Group Scenario")
scenarios = {
    'Group 1': "You’ve been paired with someone you strongly disagree with for ministering...",
    'Group 2': "You feel spiritually numb and blame church culture or others...",
    'Group 3': "The prophet said something that challenged your personal beliefs...",
    'Group 4': "A quorum member offended you months ago and never apologized..."
}
for group, scenario in scenarios.items():
    st.markdown(f"**{group} Scenario:** {scenario}")

# --- Resolution Input ---
st.header("Step 3: Submit Your Group's Resolution")
group = st.session_state.group
response = st.text_area(f"Group {group} Resolution", key="resolution_input")
if st.button("Submit Resolution"):
    st.session_state.submitted_resolutions[group] = response
    st.success("Resolution submitted.")

# --- Resolution Review & Scoring ---
if st.session_state.submitted_resolutions:
    st.header("Step 4: Score Other Group Resolutions")
    for g, r in st.session_state.submitted_resolutions.items():
        if g != group:
            st.markdown(f"### {g}'s Resolution")
            st.write(r)
            score = st.slider(f"Score for {g} (0–30)", 0, 30, key=f"score_{g}")
            st.session_state.scores[g] = score

# --- Display Results ---
if st.button("Finalize and View Scores"):
    st.header("Final Resolution Scores")
    for g, score in st.session_state.scores.items():
        st.markdown(f"**{g} Average Score:** {score}/30")
