# app.py
import streamlit as st
from PIL import Image
import pyttsx3
from streamlit_lottie import st_lottie
import requests

# ---------------- APP CONFIG ----------------
st.set_page_config(page_title="College SuperApp", layout="wide")

# ---------------- THEME & CSS ----------------
st.markdown("""
<style>
/* Page background + global font smoothing */
html, body, [class^="css"]  {
  -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;
}
/* Gradient header band */
.header-band {
  background: linear-gradient(135deg,#6c5ce7 0%, #00b894 100%);
  border-radius: 18px;
  padding: 14px 18px;
  color: white;
  box-shadow: 0 10px 22px rgba(0,0,0,.15);
  margin-bottom: 18px;
}
/* Card base */
.card {
  background: rgba(255,255,255,0.65);
  border: 1px solid rgba(255,255,255,0.35);
  border-radius: 16px;
  padding: 14px 16px;
  box-shadow: 0 6px 20px rgba(0,0,0,.08);
  backdrop-filter: blur(6px);
  transition: transform .18s ease, box-shadow .18s ease;
  margin-bottom: 12px;
}
.card:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(0,0,0,.12); }

/* Color helpers (light, subtle) */
.card-blue   { background: linear-gradient(135deg,#e8f1ff,#e6f7ff); }
.card-orange { background: linear-gradient(135deg,#fff0e0,#ffe7c9); }
.card-green  { background: linear-gradient(135deg,#e8ffe8,#dff9e2); }
.card-pink   { background: linear-gradient(135deg,#ffe6f3,#ffe9f5); }
.card-teal   { background: linear-gradient(135deg,#e6fffb,#e6fbff); }
.card-lilac  { background: linear-gradient(135deg,#efe8ff,#f2eaff); }
.card-coral  { background: linear-gradient(135deg,#ffe3de,#ffd7cc); }

/* Badge chip */
.badge {
  display: inline-block; font-size: 12px; padding: 3px 9px; border-radius: 999px;
  background: #6c5ce7; color: #fff; margin-left: 6px;
}

/* Image hover zoom */
.image-hover img {
  transition: transform .28s ease, box-shadow .28s ease;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0,0,0,.08);
}
.image-hover img:hover {
  transform: scale(1.06);
  box-shadow: 0 10px 26px rgba(0,0,0,.14);
}

/* Small title inside cards */
.card-title { font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; }
.card-text  { white-space: pre-line; margin: 0; }
</style>
""", unsafe_allow_html=True)

# ---------------- LOTTIE HELPERS ----------------
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

# Nice, safe URLs (you can swap later)
LOTTIE_WELCOME = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json")
LOTTIE_CONFETTI = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_j1adxtyb.json")
LOTTIE_LOADING  = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_jtbfg2nb.json")

# ---------------- ICONS ----------------
icons = {
    "Home": "🏠", "Student Profile": "👤", "Notes / Materials": "📄",
    "Assignments / Tasks": "📝", "Announcements": "📢", "Tools": "🛠️",
    "Student Assistant": "🧰", "College Directory": "📚",
    "Startup & Projects Hub": "🚀", "Report an Issue": "⚠️"
}

# ---------------- HEADER ----------------
# Put a logo.png in the same folder
try:
    logo = Image.open("logo.png")
    st.image(logo, width=130)
except Exception:
    st.write("")  # no logo, skip

st.markdown("<div class='header-band'><h2 style='margin:0'>Welcome to College SuperApp!</h2><p style='margin:4px 0 0 0'>Your all-in-one student companion</p></div>", unsafe_allow_html=True)
if LOTTIE_WELCOME:
    st_lottie(LOTTIE_WELCOME, speed=1, height=230, key="welcome-top")

# ---------------- SIDEBAR NAV ----------------
option = st.sidebar.selectbox(
    "Navigate",
    [f"{icons[k]} {k}" for k in icons.keys()]
)
option = option.split(" ", 1)[1]

# ---------------- CARD HELPER ----------------
def card(title: str, text: str, color_class: str = "card-blue", badge: str | None = None, image_url: str | None = None, lottie_json=None, lottie_size: int = 120):
    st.markdown(f"<div class='card {color_class}'>", unsafe_allow_html=True)

    if image_url:
        st.markdown(f"<div class='image-hover'><img src='{image_url}' width='96'></div>", unsafe_allow_html=True)

    if badge:
        st.markdown(f"<div class='card-title'>{title} <span class='badge'>{badge}</span></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='card-title'>{title}</div>", unsafe_allow_html=True)

    st.markdown(f"<p class='card-text'>{text}</p>", unsafe_allow_html=True)

    if lottie_json:
        st_lottie(lottie_json, speed=1, height=lottie_size, key=f"l_{title}_{hash(text)%10000}")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
#                         PAGES
# =========================================================

# ---------------- HOME ----------------
if option == "Home":
    st.subheader("Home")
    card("Welcome!", "Check your profile, view notes, assignments, or explore tools.", color_class="card-blue")
    if LOTTIE_WELCOME:
        st_lottie(LOTTIE_WELCOME, speed=1, height=260, key="welcome-home")

# ---------------- PROFILE ----------------
elif option == "Student Profile":
    st.subheader("Student Profile")
    c1, c2 = st.columns([1, 2], gap="large")
    with c1:
        try:
            st.image(logo, width=120)
        except Exception:
            st.write("")
    with c2:
        card("Name", "Patti Supreeth", color_class="card-orange")
        card("Roll Number", "22EG112E33", color_class="card-orange")
        card("Department", "Information Technology", color_class="card-orange")
    st.info("Tip: add your photo, links, and preferences next.")

# ---------------- NOTES ----------------
elif option == "Notes / Materials":
    st.subheader("Notes / Materials")
    uploaded_file = st.file_uploader("Upload study material", type=["pdf", "docx", "txt"])
    if uploaded_file:
        card("Uploaded File", uploaded_file.name, color_class="card-green")

# ---------------- ASSIGNMENTS ----------------
elif option == "Assignments / Tasks":
    st.subheader("Assignments / Tasks")
    tasks = [
        {"Title": "Assignment 1", "Due": "10th Sept"},
        {"Title": "Assignment 2", "Due": "15th Sept"},
    ]
    c1, c2 = st.columns(2)
    for i, t in enumerate(tasks):
        with (c1 if i % 2 == 0 else c2):
            card(t["Title"], f"Due Date: {t['Due']}", color_class="card-pink", badge="📌")

# ---------------- ANNOUNCEMENTS ----------------
elif option == "Announcements":
    st.subheader("Announcements")
    anns = [
        "College fest on 20th Sept!",
        "Mid-semester exams start from 25th Sept."
    ]
    for a in anns:
        card("Announcement", a, color_class="card-teal")

# ---------------- TOOLS ----------------
elif option == "Tools":
    st.subheader("Tools")
    tool_option = st.radio("Choose a tool", ["GPA / CGPA Calculator", "Text-to-Speech (TTS)"])

    if tool_option == "GPA / CGPA Calculator":
        sem_grades = [st.number_input(f"Semester {i}", 0.0, 10.0, 0.0, 0.1, key=f"sem{i}") for i in range(1, 9)]
        if st.button("Calculate CGPA"):
            with st.spinner("Crunching numbers..."):
                if LOTTIE_LOADING: st_lottie(LOTTIE_LOADING, speed=1, height=90, key="loading-cgpa")
            valid = [g for g in sem_grades if g > 0]
            if valid:
                cgpa = sum(valid) / len(valid)
                card("Your CGPA", f"{cgpa:.2f}", color_class="card-green", badge="🎓", lottie_json=LOTTIE_CONFETTI, lottie_size=140)
            else:
                st.error("Enter at least one semester grade.")
    else:
        tts_text = st.text_area("Enter text")
        if st.button("Speak") and tts_text.strip() != "":
            engine = pyttsx3.init()
            engine.say(tts_text)
            engine.runAndWait()
            card("Text-to-Speech", "Spoken successfully!", color_class="card-green", badge="✅")

# ---------------- STUDENT ASSISTANT ----------------
elif option == "Student Assistant":
    st.subheader("Student Assistant")
    action = st.radio("Choose", ["Attendance Alert", "Rooms Availability"])

    if action == "Attendance Alert":
        subjects = st.text_area("Enter subjects (comma separated)")
        if subjects:
            subject_list = [s.strip() for s in subjects.split(",") if s.strip()]
            attendance = {}
            for subj in subject_list:
                attendance[subj] = st.number_input(f"{subj} %", 0, 100, 0, 1, key=f"att_{subj}")
            if st.button("Check Alerts"):
                for subj, percent in attendance.items():
                    if percent < 75:
                        card(subj, f"Attendance: {percent}%", color_class="card-coral", badge="⚠️ Low")
                    else:
                        card(subj, f"Attendance: {percent}%", color_class="card-green", badge="✔️ Good")
    else:
        rooms = ["Room A101", "Room A102", "Room B201", "Lab 1", "Lab 2"]
        available = st.multiselect("Available Rooms", rooms)
        if st.button("Show Rooms"):
            if available:
                card("Available Rooms", ", ".join(available), color_class="card-orange", badge="🏫")
            else:
                st.info("No rooms selected")

# ---------------- COLLEGE DIRECTORY ----------------
elif option == "College Directory":
    st.subheader("College Directory")

    # Sample IT list (extend as needed)
    faculty_IT_full = [
        {"Name": "Dr. T. Anil Kumar",      "Designation": "Professor & HOD",     "Room": "I101", "Email": "tanilkumar@anurag.edu.in",  "Image": "https://anurag.edu.in/wp-content/uploads/2022/06/TAnilKumar.jpg"},
        {"Name": "Dr. Niteesha Sharma",    "Designation": "Assistant Professor",  "Room": "I105", "Email": "niteesha@anurag.edu.in",    "Image": "https://anurag.edu.in/wp-content/uploads/2022/06/NiteeshaSharma.jpg"},
        {"Name": "Mr. B. Pruthviraj Goud", "Designation": "Assistant Professor",  "Room": "I108", "Email": "pruthviraj@anurag.edu.in",  "Image": "https://anurag.edu.in/wp-content/uploads/2022/06/PruthvirajGoud.jpg"},
        # Add the rest of IT here…
    ]

    search = st.text_input("Search by name or designation")
    c1, c2 = st.columns(2, gap="medium")
    for i, p in enumerate(faculty_IT_full):
        if search and (search.lower() not in p["Name"].lower() and search.lower() not in p.get("Designation","").lower()):
            continue
        with (c1 if i % 2 == 0 else c2):
            card(
                title=p["Name"],
                text=f"Dept: Information Technology\nRoom: {p.get('Room','N/A')}\nEmail: {p.get('Email','N/A')}",
                badge=p.get("Designation",""),
                color_class="card-lilac",
                image_url=p.get("Image")
            )

# ---------------- STARTUP & PROJECTS HUB ----------------
elif option == "Startup & Projects Hub":
    st.subheader("Startup & Projects Hub")

    projects = [
        {"Title":"Video Surveillance","Category":"Project","Team":"A","Status":"Completed"},
        {"Title":"Academic Appraisal","Category":"Project","Team":"B","Status":"Sponsored"},
        {"Title":"College Social App","Category":"Startup","Team":"C","Status":"Seeking Mentorship"},
    ]

    search_proj = st.text_input("Search projects by title or team")

    tab_list, tab_add = st.tabs(["Projects", "Add New"])
    with tab_list:
        c1, c2 = st.columns(2, gap="large")
        for i, proj in enumerate(projects):
            if search_proj and (search_proj.lower() not in proj["Title"].lower() and search_proj.lower() not in proj.get("Team","").lower()):
                continue
            badge = {"Completed": "🎉", "Sponsored": "💰", "Seeking Mentorship": "🧑‍🏫", "Open": "🟢"}.get(proj["Status"], "")
            with (c1 if i % 2 == 0 else c2):
                card(
                    title=proj["Title"],
                    text=f"Category: {proj['Category']}\nTeam: {proj.get('Team','N/A')}\nStatus: {proj['Status']}\nDescription: {proj.get('Description','')}",
                    badge=badge,
                    color_class="card-green"
                )

    with tab_add:
        title = st.text_input("Title")
        category = st.selectbox("Category", ["Startup","Project","Research"])
        team = st.text_input("Team Members")
        status = st.selectbox("Status", ["Open","Completed","Seeking Mentorship","Sponsored"])
        description = st.text_area("Description")
        if st.button("Add Project"):
            projects.append({"Title": title, "Category": category, "Team": team, "Status": status, "Description": description})
            card(title, "Added successfully!", badge="🟢", color_class="card-green", lottie_json=LOTTIE_CONFETTI, lottie_size=140)

# ---------------- REPORT ISSUE ----------------
elif option == "Report an Issue":
    st.subheader("Report a College Issue / Maintenance")
    issue_title = st.text_input("Issue Title")
    issue_desc  = st.text_area("Description")
    category    = st.selectbox("Category",["Facilities","Classroom","Lab","Other"])
    uploaded    = st.file_uploader("Upload photo", type=["jpg","jpeg","png"])

    if st.button("Submit Issue") and issue_title.strip() and issue_desc.strip():
        card(issue_title, f"Description: {issue_desc}\nCategory: {category}", badge="⚠️", color_class="card-coral")
        if uploaded:
            st.markdown("<div class='image-hover'>", unsafe_allow_html=True)
            st.image(uploaded, caption="Uploaded Photo", use_column_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        st.info("Maintenance team will review soon.")
