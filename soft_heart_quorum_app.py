import streamlit as st
import random
from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app
import pandas as pd

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

@st.cache_resource
def init_firebase():
    import firebase_admin
    from firebase_admin import credentials, firestore
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase_service_account"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()
ADMIN_PASS = st.secrets.get("admin_password", "admin123")
st.set_page_config(page_title="Soft Heart Quorum", layout="centered")
st.markdown(
    "<style>input, textarea, button, .stSlider {font-size: 1.15em;} .stSelectbox, .stTextInput {font-size:1.1em;}</style>",
    unsafe_allow_html=True)

# --- SESSION PICKER ---
def get_sessions():
    return sorted([doc.id for doc in db.collection("sessions").stream() if not doc.to_dict().get("archived", False)])

def get_active_session():
    doc = db.collection("admin_config").document("active_session").get()
    return doc.to_dict().get("session") if doc.exists else None

def set_active_session(session):
    db.collection("admin_config").document("active_session").set({"session": session})

def ensure_session():
    sessions = get_sessions()
    active = get_active_session()
    if "session_name" not in st.session_state:
        st.write("🔑 Please join or create a session to continue.")
        if sessions:
            session_choice = st.selectbox("Select a session", sessions + ["Create new session"])
        else:
            session_choice = "Create new session"
        if session_choice == "Create new session":
            new_session = st.text_input("Enter new session name")
            if st.button("Start/Join New Session") and new_session:
                db.collection("sessions").document(new_session).set({
                    "created": datetime.now(),
                    "archived": False
                })
                st.session_state["session_name"] = new_session
                if not active:
                    set_active_session(new_session)
        else:
            if st.button("Join Session"):
                st.session_state["session_name"] = session_choice
    else:
        st.info(f"Session: {st.session_state['session_name']}")

ensure_session()
if "session_name" not in st.session_state:
    st.stop()
session_name = st.session_state["session_name"]

# --- SIDEBAR ---
st.sidebar.title("🫀 Soft Heart Quorum")
page = st.sidebar.radio(
    "Go to",
    [
        "Individual Self-Assessment",
        "Submit Group Resolution",
        "Assess Group Scenario",
        "View Scores",
        "Session Admin"
    ],
    index=0
)

# --- GROUP ASSIGNMENT WITHIN SESSION ---
def smart_assign_group():
    if "assigned_group" not in st.session_state or st.session_state.get("last_session") != session_name:
        # Get counts for this session
        group_counts = {}
        for group in GROUPS:
            doc = db.collection("sessions").document(session_name).collection("group_assignments").document(group).get()
            data = doc.to_dict()
            group_counts[group] = data["count"] if data and "count" in data else 0
        # Find group(s) with minimum count
        min_count = min(group_counts.values())
        min_groups = [g for g, cnt in group_counts.items() if cnt == min_count]
        assigned = random.choice(min_groups)
        doc_ref = db.collection("sessions").document(session_name).collection("group_assignments").document(assigned)
        doc_ref.set({"count": group_counts[assigned] + 1})
        st.session_state["assigned_group"] = assigned
        st.session_state["last_session"] = session_name
    return st.session_state["assigned_group"]

# --- INDIVIDUAL SELF-ASSESSMENT ---
if page == "Individual Self-Assessment":
    st.header("🧍 Personal Spiritual Softness Check")
    st.write("Reflect on your heart this week:")
    with st.form("individual_assessment_form"):
        name = st.text_input("Your Name (optional, for encouragement)")
        score = 0
        slider_vals = []
        for q in PERSONAL_QUESTIONS:
            val = st.slider(q, 0, 3, 1, key=q+session_name)
            score += val
            slider_vals.append(val)
        submitted = st.form_submit_button("Submit Assessment")
        if submitted:
            db.collection("sessions").document(session_name).collection("individual_assessments").add({
                "name": name,
                "answers": slider_vals,
                "score": score,
                "timestamp": datetime.now()
            })
            st.markdown(f"### 💬 Your Score: **{score}/30**")
            if score >= 25:
                st.success("Your heart is soft and open to the Spirit.")
            elif score >= 18:
                st.warning("You're on the path — keep softening your heart daily.")
            else:
                st.error("Time to return to the Lord with full purpose of heart.")

# --- SUBMIT GROUP RESOLUTION ---
elif page == "Submit Group Resolution":
    st.header("📘 Submit Group Resolution")
    group = smart_assign_group()
    st.info(f"**You are in: {group}**")
    st.markdown(f"**Scenario:** {SCENARIOS[group]}")
    with st.form("group_resolution_form"):
        group_name = group
        resolution_text = st.text_area("What is your group's resolution?", height=100)
        submitted = st.form_submit_button("Submit Resolution")
        if submitted and resolution_text.strip():
            db.collection("sessions").document(session_name).collection("group_resolutions").document(group_name).set({
                "resolution": resolution_text,
                "timestamp": datetime.now()
            })
            st.success("✅ Group resolution submitted.")

# --- ASSESS GROUP SCENARIO ---
elif page == "Assess Group Scenario":
    st.header("📝 Assess Group Scenario Resolutions")
    selected_group = st.selectbox("Select a group to assess:", GROUPS)
    st.markdown(f"**Scenario:** {SCENARIOS[selected_group]}")
    res_doc = db.collection("sessions").document(session_name).collection("group_resolutions").document(selected_group).get()
    resolution = res_doc.to_dict()["resolution"] if res_doc.exists else None
    if resolution:
        st.success(f"**Group Resolution:** {resolution}")
        with st.form(f"group_assessment_form_{selected_group}"):
            scores = []
            for i, q in enumerate(GROUP_ASSESSMENT_QUESTIONS):
                val = st.slider(f"{i+1}. {q}", 0, 3, 1, key=f"{selected_group}_groupq{i}_{session_name}")
                scores.append(val)
            submit = st.form_submit_button("Submit Assessment")
            if submit:
                db.collection("sessions").document(session_name).collection("group_assessments").add({
                    "group": selected_group,
                    "scores": scores,
                    "timestamp": datetime.now()
                })
                st.success("✅ Assessment submitted!")
    else:
        st.warning("No resolution has been submitted by this group yet.")

# --- ADMIN SCORES PAGE ---
elif page == "View Scores":
    st.header("📊 Assessment Summary")
    pw = st.text_input("Enter Admin Password", type="password")
    if pw != ADMIN_PASS:
        st.warning("🔒 Enter correct password to view scores.")
        st.stop()

    st.subheader("Group Assessments")
    ga_docs = db.collection("sessions").document(session_name).collection("group_assessments").stream()
    rows = []
    for doc in ga_docs:
        d = doc.to_dict()
        if "group" in d and "scores" in d:
            rows.append([d["group"]] + d["scores"])
    if rows:
        group_df = pd.DataFrame(rows, columns=["Group"] + [f"Q{i+1}" for i in range(len(GROUP_ASSESSMENT_QUESTIONS))])
        group_df["Avg"] = group_df.iloc[:, 1:].mean(axis=1)
        st.dataframe(group_df)
    else:
        st.info("No group assessments yet.")

    st.subheader("Individual Assessments")
    ia_docs = db.collection("sessions").document(session_name).collection("individual_assessments").stream()
    rows = []
    for doc in ia_docs:
        d = doc.to_dict()
        if "name" in d and "answers" in d:
            rows.append([d.get("name", "")] + d["answers"] + [d["score"]])
    if rows:
        indiv_df = pd.DataFrame(rows, columns=["Name"] + [f"Q{i+1}" for i in range(len(PERSONAL_QUESTIONS))] + ["Total"])
        st.dataframe(indiv_df)
    else:
        st.info("No individual assessments yet.")

# --- SESSION ADMIN PAGE ---
elif page == "Session Admin":
    st.header("⚙️ Session Management (Admin)")
    pw = st.text_input("Admin Password", type="password", key="adminpw")
    if pw != ADMIN_PASS:
        st.warning("🔒 Enter correct password for session management.")
        st.stop()

    st.subheader("Existing Sessions")
    sessions = get_sessions()
    active_session = get_active_session()
    for sess in sessions:
        col1, col2, col3 = st.columns([4,2,2])
        col1.markdown(f"**{sess}** {'(Active)' if sess == active_session else ''}")
        if col2.button(f"Set Active", key=f"set_{sess}"):
            set_active_session(sess)
            st.success(f"Session {sess} set as active!")
        if col3.button(f"Archive", key=f"archive_{sess}"):
            db.collection("sessions").document(sess).set({"archived": True}, merge=True)
            st.success(f"Session {sess} archived!")
