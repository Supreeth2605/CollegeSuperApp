import streamlit as st
from PIL import Image
import pyttsx3
from streamlit_lottie import st_lottie
import requests

# --- APP CONFIG ---
st.set_page_config(page_title="College SuperApp", layout="wide")

# --- LOAD LOTTIE ANIMATION ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Lottie URLs
welcome_animation = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json") # Floating books/students
celebration_animation = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_j1adxtyb.json") # Confetti
loading_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_jtbfg2nb.json") # Loading

# --- ICONS ---
icons = {
    "Home": "🏠", "Student Profile": "👤", "Notes / Materials": "📄",
    "Assignments / Tasks": "📝", "Announcements": "📢", "Tools": "🛠️",
    "Student Assistant": "🧰", "College Directory": "📚",
    "Startup & Projects Hub": "🚀", "Report an Issue": "⚠️"
}

# --- LOGO ---
logo = Image.open("logo.png")
st.image(logo, width=150)
st.title("Welcome to College SuperApp!")
st.subheader("Your all-in-one student companion app for college life")
st_lottie(welcome_animation, speed=1, width=350, height=350, key="welcome")
st.write("---")

# --- SIDEBAR NAVIGATION ---
option = st.sidebar.selectbox(
    "Navigate",
    [f"{icons[k]} {k}" for k in icons.keys()]
)
option = option.split(" ", 1)[1]

# --- CARD FUNCTION WITH COLORS AND LOTTIE ---
def display_card(title, content, badge=None, color="#a1caff", image_url=None, lottie=None):
    with st.container():
        if image_url:
            st.image(image_url, width=80)
        if badge:
            st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:15px'>**{title} [{badge}]**</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:15px'>**{title}**</div>", unsafe_allow_html=True)
        st.caption(content)
        if lottie:
            st_lottie(lottie, speed=1, width=150, height=150)

# --- HOME PAGE ---
if option == "Home":
    st.header("Home")
    st.subheader("Welcome!")
    st.caption("Check your profile, view notes, assignments, or explore tools.")
    st_lottie(welcome_animation, speed=1, width=300, height=300)

# --- STUDENT PROFILE PAGE ---
elif option == "Student Profile":
    st.header("Student Profile")
    col1, col2 = st.columns([1,2])
    with col1:
        st.image(logo, width=120)
    with col2:
        st.subheader("Name: Patti Supreeth")
        st.subheader("Roll Number: 22EG112E33")
        st.subheader("Department: Information Technology")
    st.info("Expand with more details, photos, and settings.")

# --- NOTES / MATERIALS PAGE ---
elif option == "Notes / Materials":
    st.header("Notes / Materials")
    uploaded_file = st.file_uploader("Upload study material", type=["pdf","docx","txt"])
    if uploaded_file:
        display_card("Uploaded File", uploaded_file.name, color="#d4f4dd")

# --- ASSIGNMENTS / TASKS PAGE ---
elif option == "Assignments / Tasks":
    st.header("Assignments / Tasks")
    tasks = [{"Title":"Assignment 1","Due":"10th Sept"},{"Title":"Assignment 2","Due":"15th Sept"}]
    for task in tasks:
        display_card(task['Title'], f"Due Date: {task['Due']}", color="#ffe0f0", badge="📌")

# --- ANNOUNCEMENTS PAGE ---
elif option == "Announcements":
    st.header("Announcements")
    announcements = ["College fest on 20th Sept!","Mid-semester exams start from 25th Sept."]
    for ann in announcements:
        display_card("Announcement", ann, color="#a1caff")

# --- TOOLS PAGE ---
elif option == "Tools":
    st.header("Tools")
    tool_option = st.radio("Choose a tool", ["GPA / CGPA Calculator", "Text-to-Speech (TTS)"])
    if tool_option=="GPA / CGPA Calculator":
        sem_grades = [st.number_input(f"Semester {i}",0.0,10.0,0.1,key=f"sem{i}") for i in range(1,9)]
        if st.button("Calculate CGPA"):
            with st.spinner("Calculating..."):
                st_lottie(loading_animation, speed=1, width=100, height=100)
            valid_grades = [g for g in sem_grades if g>0]
            if valid_grades:
                cgpa = sum(valid_grades)/len(valid_grades)
                display_card("Your CGPA", f"{cgpa:.2f}", color="#caffbf", lottie=celebration_animation)
            else: st.error("Enter at least one semester grade.")
    else:
        tts_text = st.text_area("Enter text")
        if st.button("Speak") and tts_text.strip()!="":
            engine=pyttsx3.init(); engine.say(tts_text); engine.runAndWait()
            st.success("Spoken successfully!")

# --- STUDENT ASSISTANT PAGE ---
elif option=="Student Assistant":
    st.header("Student Assistant")
    assistant_option = st.radio("Choose", ["Attendance Alert","Rooms Availability"])
    if assistant_option=="Attendance Alert":
        subjects = st.text_area("Enter subjects comma separated")
        if subjects:
            subject_list=[s.strip() for s in subjects.split(",")]
            attendance={}; 
            for subj in subject_list: attendance[subj]=st.number_input(f"{subj}%",0,100,1,key=subj)
            if st.button("Check Alerts"):
                for subj,percent in attendance.items():
                    if percent<75:
                        display_card(subj, f"Attendance: {percent}%", color="#ff6b6b", badge="⚠️ Low")
                    else:
                        display_card(subj, f"Attendance: {percent}%", color="#90ee90", badge="✔️ Good")
    else:
        rooms=["Room A101","Room A102","Room B201","Lab 1","Lab 2"]
        available=st.multiselect("Available Rooms",rooms)
        if st.button("Show Rooms"):
            if available: display_card("Available Rooms", ", ".join(available), color="#ffd6a5", badge="🏫")
            else: st.info("No rooms selected")

# --- COLLEGE DIRECTORY PAGE ---
elif option=="College Directory":
    st.header("College Directory")

    faculty_IT_full = [
        {"Name":"Dr. T. Anil Kumar","Designation":"Professor & HOD","Room":"I101","Email":"tanilkumar@anurag.edu.in","Image":"https://anurag.edu.in/wp-content/uploads/2022/06/TAnilKumar.jpg"},
        {"Name":"Dr. Niteesha Sharma","Designation":"Assistant Professor","Room":"I105","Email":"niteesha@anurag.edu.in","Image":"https://anurag.edu.in/wp-content/uploads/2022/06/NiteeshaSharma.jpg"},
        {"Name":"Mr. B. Pruthviraj Goud","Designation":"Assistant Professor","Room":"I108","Email":"pruthviraj@anurag.edu.in","Image":"https://anurag.edu.in/wp-content/uploads/2022/06/PruthvirajGoud.jpg"}
        # Add all remaining IT faculty here
    ]

    search = st.text_input("Search by name or designation")
    for person in faculty_IT_full:
        if search.lower() not in person['Name'].lower() and search.lower() not in person.get("Designation","").lower():
            continue
        display_card(
            title=person['Name'],
            content=f"Dept: IT\nRoom: {person.get('Room','N/A')}\nEmail: {person.get('Email','N/A')}",
            badge=person.get("Designation",""),
            color="#d1c4e9",
            image_url=person.get("Image")
        )

# --- STARTUP & PROJECTS HUB ---
elif option=="Startup & Projects Hub":
    st.header("Startup & Projects Hub")
    projects=[{"Title":"Video Surveillance","Category":"Project","Team":"A","Status":"Completed"},
              {"Title":"Academic Appraisal","Category":"Project","Team":"B","Status":"Sponsored"},
              {"Title":"College Social App","Category":"Startup","Team":"C","Status":"Seeking Mentorship"}]
    search_proj=st.text_input("Search projects by title or team")
    tab1, tab2 = st.tabs(["Projects", "Add New"])
    with tab1:
        for proj in projects:
            if search_proj.lower() not in proj['Title'].lower() and search_proj.lower() not in proj.get("Team","").lower(): continue
            badge = {"Completed":"🎉","Sponsored":"💰","Seeking Mentorship":"🧑‍🏫","Open":"🟢"}.get(proj['Status'],"")
            display_card(
                title=proj['Title'],
                content=f"Category: {proj['Category']}\nTeam: {proj.get('Team','N/A')}\nStatus: {proj['Status']}\nDescription: {proj.get('Description','')}",
                badge=badge,
                color="#c8e6c9"
            )
    with tab2:
        title=st.text_input("Title"); category=st.selectbox("Category",["Startup","Project","Research"])
        team=st.text_input("Team Members"); status=st.selectbox("Status",["Open","Completed","Seeking Mentorship","Sponsored"])
        description=st.text_area("Description")
        if st.button("Add Project"): projects.append({"Title":title,"Category":category,"Team":team,"Status":status,"Description":description}); display_card(title,f"Added successfully!",badge="🟢",lottie=celebration_animation,color="#c8e6c9")

# --- REPORT ISSUE ---
elif option=="Report an Issue":
    st.header("Report a College Issue / Maintenance")
    issue_title=st.text_input("Issue Title")
    issue_desc=st.text_area("Description")
    category=st.selectbox("Category",["Facilities","Classroom","Lab","Other"])
    uploaded_image=st.file_uploader("Upload photo",type=["jpg","png","jpeg"])
    if st.button("Submit Issue") and issue_title.strip()!="" and issue_desc.strip()!="":
        display_card(issue_title,f"Description: {issue_desc}\nCategory: {category}",badge="⚠️",color="#ff8a65")
        if uploaded_image: st.image(uploaded_image, caption="Uploaded Photo", use_column_width=True)
        st.info("Maintenance team will review soon.")
