
import streamlit as st
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
import pandas as pd

# === Initialize Firebase ===
@st.cache_resource
def init_firebase():
    cred = credentials.Certificate(st.secrets["firebase_service_account"])
    initialize_app(cred)
    return firestore.client()

db = init_firebase()

# === Admin Password ===
ADMIN_PASS = st.secrets.get("admin_password", "admin123")

# === Sidebar Navigation ===
st.sidebar.title("🫀 Soft Heart Quorum")
page = st.sidebar.radio("Go to", ["Submit Resolution", "Assess Groups", "View Scores"])

# === Resolution Submission ===
if page == "Submit Resolution":
    st.title("📘 Group Resolution Submission")
    with st.form("submit_resolution"):
        group_name = st.text_input("Group Name")
        resolution_text = st.text_area("What is your group's resolution?")
        submitted = st.form_submit_button("Submit")
        if submitted and group_name and resolution_text:
            db.collection("group_resolutions").document(group_name).set({
                "resolution": resolution_text,
                "timestamp": datetime.now()
            })
            st.success(f"✅ Resolution saved for {group_name}.")

# === Group Assessments ===
elif page == "Assess Groups":
    st.title("📝 Group Resolution Assessment")
    resolutions = db.collection("group_resolutions").stream()
    for doc in resolutions:
        group = doc.id
        resolution = doc.to_dict().get("resolution", "")
        st.markdown(f"### 🧾 {group}")
        st.info(resolution)

        with st.form(f"form_{group}"):
            humility = st.slider("1. Does this reflect humility?", 1, 5)
            forgiveness = st.slider("2. Does this promote forgiveness?", 1, 5)
            empathy = st.slider("3. Does this involve listening or empathy?", 1, 5)
            spirituality = st.slider("4. Is it spiritually motivated?", 1, 5)
            peacemaking = st.slider("5. Does it encourage peacemaking?", 1, 5)
            submit = st.form_submit_button("Submit Assessment")
            if submit:
                db.collection("group_assessments").add({
                    "group": group,
                    "humility": humility,
                    "forgiveness": forgiveness,
                    "empathy": empathy,
                    "spirituality": spirituality,
                    "peacemaking": peacemaking,
                    "timestamp": datetime.now()
                })
                st.success(f"✅ Assessment for {group} submitted.")

# === Admin Dashboard ===
elif page == "View Scores":
    st.title("📊 Assessment Summary")
    pw = st.text_input("Enter Admin Password", type="password")
    if pw != ADMIN_PASS:
        st.warning("🔒 Enter correct password to view scores.")
        st.stop()

    assessments = db.collection("group_assessments").stream()
    rows = [a.to_dict() for a in assessments]
    if rows:
        df = pd.DataFrame(rows)
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
        st.dataframe(df)

        avg_df = df.groupby("group")[["humility", "forgiveness", "empathy", "spirituality", "peacemaking"]].mean()
        avg_df["average_score"] = avg_df.mean(axis=1)
        st.subheader("📈 Group Average Scores")
        st.dataframe(avg_df)

        csv = avg_df.reset_index().to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, "group_scores.csv", "text/csv")
    else:
        st.info("No assessments available yet.")
