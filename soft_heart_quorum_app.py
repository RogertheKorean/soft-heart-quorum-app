import streamlit as st
from streamlit_autorefresh import st_autorefresh
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import random
import json

GROUPS = ["Group 1", "Group 2", "Group 3", "Group 4"]
SCENARIOS = {
    "Group 1": "You’ve been assigned to minister with someone you strongly disagree with politically. You're now asked to give a joint message together. How do you approach this?",
    "Group 2": "You’ve felt spiritually numb for months. At church, you often think others are fake or overly judgmental. A new member asks you for help. What do you do?",
    "Group 3": "A recent talk by the prophet directly challenged your personal views. You feel conflicted and upset, and now you're leading the lesson on that topic. How do you respond?",
    "Group 4": "A quorum member offended you deeply several months ago. You never addressed it, and now you're both assigned to teach together this Sunday. What do you do?"
}
PERSONAL_QUESTIONS = [
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
GROUP_ASSESSMENT_QUESTIONS = [
    "Did this response reflect a spirit of sincere repentance?",
    "Does this response align with gospel principles found in the scriptures?",
    "Does the resolution show thoughtful, prayerful consideration?",
    "Does it reflect submission to God's will over personal preferences?",
    "Does it promote forgiveness and reconciliation?",
    "Does it reflect a willingness to serve even when it's uncomfortable or hard?",
    "Does it bear or invite a testimony of Christ or gospel truth?",
    "Does it follow prophetic guidance as taught in the talk?",
    "Does it show openness to correction, feedback, or new understanding?",
    "Is there evidence of following promptings or spiritual impressions in this resolution?"
]

st.set_page_config(page_title="Soft Heart Quorum App", layout="centered")
st_autorefresh(interval=10000, key="refresh")

if "group" not in st.session_state:
    st.session_state.group = random.choice(GROUPS)
if "personal_scores" not in st.session_state:
    st.session_state.personal_scores = [0]*10
if "evaluator_id" not in st.session_state:
    st.session_state.evaluator_id = str(random.randint(10000, 99999))
if "scoring_unlocked" not in st.session_state:
    st.session_state.scoring_unlocked = False

# Load credentials from Streamlit secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1FiEvYoda8_eygtuF9wxE65fmk1rukUP79BjS8r4ivxs")

res_ws = sheet.sheet1
try:
    score_ws = sheet.worksheet("Scores")
except:
    score_ws = sheet.add_worksheet(title="Scores", rows="100", cols="20")
    score_ws.append_row(["evaluator_id", "group_scored"] + [f"q{i+1}" for i in range(10)] + ["total", "timestamp"])

st.title("🧡 Soften Your Heart – Quorum Activity App")

pw = st.text_input("🔐 Facilitator password to unlock group scoring:", type="password")
if pw == "facilitator123":
    st.session_state.scoring_unlocked = True
    st.success("Scoring is now enabled.")

st.header("🧍‍♂️ My Soft Heart Check (Private)")
with st.form("personal_form"):
    for i, q in enumerate(PERSONAL_QUESTIONS):
        st.session_state.personal_scores[i] = st.slider(f"{i+1}. {q}", 0, 3, value=st.session_state.personal_scores[i], key=f"personal_{i}")
    st.form_submit_button("Save My Reflection")

st.header("🤝 Group Resolution")
group = st.session_state.group
scenario = SCENARIOS[group]
st.markdown(f"**You are in {group}**")
st.info(scenario)

all_res = res_ws.get_all_records()
existing = {row['group']: row['resolution'] for row in all_res}
submitted = existing.get(group, "")

if not st.session_state.scoring_unlocked:
    with st.form("res_form"):
        content = st.text_area("✍️ Your group's response:", value=submitted)
        if st.form_submit_button("Submit / Update"):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated = False
            for i, row in enumerate(all_res):
                if row["group"] == group:
                    res_ws.update(f"B{i+2}", [[content]])
                    res_ws.update(f"C{i+2}", [[timestamp]])
                    updated = True
            if not updated:
                res_ws.append_row([group, content, timestamp])
            st.success("✅ Response saved!")

else:
    st.subheader("📝 All Group Responses")
    for g in GROUPS:
        if g in existing:
            with st.expander(f"{g} – Click to View"):
                st.markdown(f"**Scenario:** {SCENARIOS[g]}")
                st.code(existing[g], language="markdown")

    st.header("🗳️ Score Other Groups")
    for g in GROUPS:
        if g != group and g in existing:
            scored = score_ws.findall(st.session_state.evaluator_id)
            already = any(g == row.value for row in scored if row.col == 2)
            if not already:
                with st.form(f"score_{g}"):
                    scores = [st.slider(f"{i+1}. {q}", 0, 3, key=f"{g}_{i}") for i, q in enumerate(GROUP_ASSESSMENT_QUESTIONS)]
                    if st.form_submit_button("Submit Score"):
                        total = sum(scores)
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        score_ws.append_row([st.session_state.evaluator_id, g] + scores + [total, timestamp])
                        st.success("Score submitted!")
            else:
                st.info(f"✅ You’ve already scored {g}")
