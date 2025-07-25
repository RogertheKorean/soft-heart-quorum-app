import streamlit as st
import random

# --- Constants ---
GROUPS = ["Group 1", "Group 2", "Group 3", "Group 4"]
SCENARIOS = {
    "Group 1": "You’ve been assigned to minister with someone you strongly disagree with politically. You're now asked to give a joint message together. How do you approach this?",
    "Group 2": "You’ve felt spiritually numb for months. At church, you often think others are fake or overly judgmental. A new member asks you for help. What do you do?",
    "Group 3": "A recent talk by the prophet directly challenged your personal views. You feel conflicted and upset, and now you're leading the lesson on that topic. How do you respond?",
    "Group 4": "A quorum member offended you deeply several months ago. You never addressed it, and now you're both assigned to teach together this Sunday. What do you do?"
}
QUESTIONS = [
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

# --- Session State Init ---
if "group" not in st.session_state:
    st.session_state.group = random.choice(GROUPS)
if "submitted_resolutions" not in st.session_state:
    st.session_state.submitted_resolutions = {}
if "scoring_unlocked" not in st.session_state:
    st.session_state.scoring_unlocked = False
if "completed_scores" not in st.session_state:
    st.session_state.completed_scores = {}
if "final_scores" not in st.session_state:
    st.session_state.final_scores = {}

# --- Title & Password ---
st.title("🧡 Soften Your Heart – Quorum Scenario Activity")
pw = st.text_input("🔐 Facilitator password to unlock scoring:", type="password")
if pw == "facilitator123":
    st.success("Scoring is now enabled.")
    st.session_state.scoring_unlocked = True
elif pw and not st.session_state.scoring_unlocked:
    st.error("Incorrect password.")

# --- Group Display ---
my_group = st.session_state.group
st.markdown(f"### You are in **{my_group}**")
st.info(SCENARIOS[my_group])

# --- Resolution Submission ---
st.header("✍️ Your Group's Resolution")
if not st.session_state.scoring_unlocked:
    with st.form("resolution_form"):
        res_text = st.text_area("Write your group's response here:", value=st.session_state.submitted_resolutions.get(my_group, ""))
        submit = st.form_submit_button("Save / Update")
        if submit:
            st.session_state.submitted_resolutions[my_group] = res_text
            st.success("Resolution saved.")
else:
    st.write("Your submitted resolution:")
    st.code(st.session_state.submitted_resolutions.get(my_group, "Not submitted yet."), language="markdown")

# --- Group Resolution Queue ---
if st.session_state.scoring_unlocked:
    st.header("🗳️ Score Other Group Resolutions")
    for g in GROUPS:
        if g != my_group and g in st.session_state.submitted_resolutions:
            with st.expander(f"🔍 {g}'s Resolution"):
                st.markdown(f"**Scenario:** {SCENARIOS[g]}")
                st.markdown(f"**Resolution:**\n\n{st.session_state.submitted_resolutions[g]}")

                if g not in st.session_state.completed_scores:
                    with st.form(f"score_{g}"):
                        scores = []
                        for i, q in enumerate(QUESTIONS):
                            scores.append(st.slider(f"{i+1}. {q}", 0, 3, key=f"{g}_q{i}"))
                        submit_score = st.form_submit_button("Submit Score")
                        if submit_score:
                            st.session_state.completed_scores[g] = scores
                            st.success(f"Scores for {g} recorded.")
                else:
                    st.info(f"✅ You have already scored {g}.")
                    st.write("Your Scores:")
                    for i, score in enumerate(st.session_state.completed_scores[g]):
                        st.write(f"{i+1}. {QUESTIONS[i]} — {score}")

    # Final Summary
    if len(st.session_state.completed_scores) == 3:
        st.header("📊 Final Score Summary")
        for g, score_list in st.session_state.completed_scores.items():
            total = sum(score_list)
            st.markdown(f"**{g}**: {total} points")
