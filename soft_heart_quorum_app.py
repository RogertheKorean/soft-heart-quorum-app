
import streamlit as st
import random

# Session setup
if "group" not in st.session_state:
    st.session_state.group = random.choice(["Group 1", "Group 2", "Group 3", "Group 4"])
if "submitted_resolutions" not in st.session_state:
    st.session_state.submitted_resolutions = {}
if "scoring_unlocked" not in st.session_state:
    st.session_state.scoring_unlocked = False
if "completed_scores" not in st.session_state:
    st.session_state.completed_scores = []

# Facilitator unlock
st.title("🧡 Soften Your Heart – Quorum Activity")
facilitator_pw = st.text_input("🔑 Enter facilitator password to unlock group scoring:", type="password")
if facilitator_pw == "facilitator123":
    st.success("✅ Scoring is now enabled.")
    st.session_state.scoring_unlocked = True
elif facilitator_pw:
    st.error("Incorrect password.")

st.markdown(f"### You are in **{st.session_state.group}**")

# Soft heart assessment
st.header("Step 1: Heart Softness Assessment")
questions = [
    "Do I sincerely repent each day?",
    "Do I study the scriptures regularly?",
    "Do I pray with intent and listen?",
    "Do I submit my will to God's?",
    "Do I forgive those who hurt me?",
    "Do I serve even when it’s inconvenient?",
    "Do I share my testimony regularly?",
    "Do I follow prophetic counsel?",
    "Am I open to correction or redirection?",
    "Do I recognize and follow spiritual promptings?"
]
total_score = 0
for q in questions:
    total_score += st.slider(q, 0, 3, key=q)

st.markdown(f"#### Your Heart Softness Score: **{total_score}/30**")

# Scenario display
scenarios = {
    "Group 1": "You’ve been paired with someone you strongly disagree with for ministering...",
    "Group 2": "You feel spiritually numb and blame church culture or others...",
    "Group 3": "The prophet said something that challenged your personal beliefs...",
    "Group 4": "A quorum member offended you months ago and never apologized..."
}
group = st.session_state.group
st.subheader("📘 Your Group Scenario")
st.write(scenarios[group])

with st.form("submit_resolution"):
    resolution_text = st.text_area("✍️ Your Group's Resolution", value=st.session_state.submitted_resolutions.get(group, ""))
    submitted = st.form_submit_button("Submit / Update Resolution")
    if submitted and not st.session_state.scoring_unlocked:
        st.session_state.submitted_resolutions[group] = resolution_text
        st.success("Resolution saved.")

# Scoring section
if st.session_state.scoring_unlocked:
    st.header("Step 2: Score Other Groups' Resolutions")
    for g, res in st.session_state.submitted_resolutions.items():
        if g != group:
            with st.expander(f"{g}'s Resolution"):
                st.write(res)
                if g not in st.session_state.completed_scores:
                    with st.form(f"score_{g}"):
                        score = st.slider(f"Score for {g} (0–30)", 0, 30)
                        submit_score = st.form_submit_button("Submit Score")
                        if submit_score:
                            st.session_state.completed_scores.append(g)
                            st.success(f"Score for {g} recorded.")
                else:
                    st.info(f"You have already scored {g}. ✅")

    if len(st.session_state.completed_scores) == 3:
        st.header("📊 Final Resolution Scores")
        for g in st.session_state.completed_scores:
            st.write(f"✅ {g} – Score recorded.")
