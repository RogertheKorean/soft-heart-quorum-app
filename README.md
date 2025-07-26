🫀 Soft Heart Quorum App
A Streamlit + Firebase web application for Elders Quorum (or other groups) to self-assess, resolve group scenarios, and manage all participation “by session.”

Session-based: Every event, lesson, or group meeting is kept separate—no data is lost!

Admin features: Manage sessions, set active, and archive old sessions.

Automatic group balancing: Group assignments ensure even distribution as new users join.

Mobile-first UI: Easy for all participants to use on phone or tablet.

🚀 Features
Session management: Each meeting/activity uses a unique session name. All data is kept for review or export.

Group scenario assignment: Each participant is assigned to a group, with balanced logic—first 4 users fill all groups, then fill evenly after.

Self and group assessment:

10 personal “soft heart” questions, 0–3 slider, live feedback.

Group scenario with 10 custom group assessment questions, 0–3 slider.

Admin dashboard:

Set which session is “active” (for all new joiners).

Archive (hide) old sessions from public picker.

View/compare scores and results per session.

All data is live and updates immediately.

🛠️ Setup
1. Firebase Setup
Create a Firebase project and Firestore DB.

Download your service account JSON key.

In Streamlit Cloud or locally, use this as your firebase_service_account secret.

2. Secrets Configuration
secrets.toml (Streamlit Cloud):

toml
Copy
Edit
[firebase_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
universe_domain = "googleapis.com"

admin_password = "your_admin_password"
3. Install Python dependencies
bash
Copy
Edit
pip install streamlit firebase-admin pandas
4. Run the App
bash
Copy
Edit
streamlit run your_app.py
🎯 Usage Flow
Select or Create a Session:
Users (and admin) pick the session for this event/lesson. Sessions keep all data separate and organized.

Submit Group Resolution:
Each participant is assigned to a group (Group 1–4, balanced logic).
The group discusses and submits a resolution to their scenario.

Group Scenario Assessment:
Any user can assess any group’s submitted resolution (select from dropdown).

Individual Self-Assessment:
Each user reflects and rates themselves on 10 spiritual “soft heart” questions.

Admin Management:

Admin can set which session is currently “active” (the default for all joiners).

Archive old sessions (hides from users, keeps for admin/history).

View results for all group and individual assessments per session.

📱 Mobile UX
All forms, sliders, and buttons are full width.

Minimal horizontal scrolling required.

Use on phone or tablet is easy.

🔒 Data & Privacy
All participation is tied to session name.

No personally identifying data is required (names are optional).

No data is ever deleted automatically; admin can archive but not destroy data.

👨‍💼 Admin Quickstart
Log in to the Session Admin page with your password.

Set or create the active session for your event.

Archive any past sessions to keep the session picker clean.

View all results live.

🏆 Future Ideas
Export scores/results to CSV for each session.

Participant analytics (group/individual trends).

Gamification or “streaks” for participation.

Custom branding and further localization.

🙏 Credit
Developed with ChatGPT guidance for a real-world LDS quorum use case.
Contact: [Roger Park]

