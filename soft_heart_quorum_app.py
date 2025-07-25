
import streamlit as st
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime

@st.cache_resource
def init_firebase():
    cred = credentials.Certificate(st.secrets["firebase_service_account"])
    initialize_app(cred)
    return firestore.client()

db = init_firebase()

def save_group_resolution(group_name, resolution_text):
    doc_ref = db.collection("group_resolutions").document(group_name)
    doc_ref.set({
        "resolution": resolution_text,
        "timestamp": datetime.now()
    })

def fetch_all_group_resolutions():
    docs = db.collection("group_resolutions").stream()
    return {doc.id: doc.to_dict() for doc in docs}

# Main app
st.title("🫀 Soft Heart Quorum")

# Submit resolution section
with st.form("submit_resolution"):
    group_name = st.text_input("Group Name")
    resolution_text = st.text_area("Your group's resolution")
    submitted = st.form_submit_button("Submit Resolution")
    if submitted and group_name and resolution_text:
        save_group_resolution(group_name, resolution_text)
        st.success(f"Resolution for {group_name} saved!")

# Assessment section
st.header("📝 Group Resolution Assessments")
group_responses = fetch_all_group_resolutions()

for group, data in group_responses.items():
    st.markdown(f"### 🧾 {group}")
    st.info(data.get("resolution", "No resolution provided."))

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
            st.success("Assessment submitted.")
