import streamlit as st
from PIL import Image
import pyttsx3

# --- APP CONFIG ---
st.set_page_config(page_title="College SuperApp", layout="wide")

# --- ICONS ---
icons = {
    "Home": "🏠", "Student Profile": "👤", "Notes / Materials": "📄",
    "Assignments / Tasks": "📝", "Announcements": "📢", "Tools": "🛠️",
    "Student Assistant": "🧰", "College Directory": "📚",
    "Startup & Projects Hub": "🚀", "Report an Issue": "⚠️"
}

# --- LOGO ---
logo = Image.open("logo.png")  # Make sure this file is in the same folder
st.image(logo, width=150)
st.markdown("<h1 style='text-align:center'>Welcome to College SuperApp!</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Your all-in-one student companion app for college life</p>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR NAVIGATION ---
option = st.sidebar.selectbox(
    "Navigate",
    [f"{icons[k]} {k}" for k in icons.keys()]
)
option = option.split(" ",1)[1]  # remove icon for internal use

# --- FUNCTION TO DISPLAY CARDS WITH BADGES ---
def display_card(title, content, color="lightblue", badge=None):
    badge_html = f"<span style='background-color:#ff6b6b;color:white;padding:3px 8px;border-radius:8px;margin-left:5px'>{badge}</span>" if badge else ""
    st.markdown(f"""
    <div style='background-color:{color}; padding:15px; border-radius:10px; margin-bottom:10px'>
        <h4>{title} {badge_html}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

# --- HOME PAGE ---
if option == "Home":
    st.header("Home")
    display_card("Welcome!", "Check your profile, view notes, assignments, or explore tools.", color="#a1caff")

# --- STUDENT PROFILE PAGE ---
elif option == "Student Profile":
    st.header("Student Profile")
    col1, col2 = st.columns([1,2])
    with col1:
        st.image(logo, width=120)
    with col2:
        display_card("Name", "Patti Supreeth", color="#ffd6a5")
        display_card("Roll Number", "22EG112E33", color="#ffd6a5")
        display_card("Department", "Information Technology", color="#ffd6a5")
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
            valid_grades = [g for g in sem_grades if g>0]
            if valid_grades:
                cgpa = sum(valid_grades)/len(valid_grades)
                display_card("Your CGPA", f"{cgpa:.2f}", color="#caffbf", badge="🎓")
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
                    color="#ff6b6b" if percent<75 else "#90ee90"
                    badge="⚠️ Low" if percent<75 else "✔️ Good"
                    display_card(subj,f"Attendance: {percent}%",color=color,badge=badge)
    else:
        rooms=["Room A101","Room A102","Room B201","Lab 1","Lab 2"]
        available=st.multiselect("Available Rooms",rooms)
        if st.button("Show Rooms"):
            if available: display_card("Available Rooms",", ".join(available),color="#ffd6a5",badge="🏫")
            else: st.info("No rooms selected")

# --- COLLEGE DIRECTORY PAGE ---
elif option=="College Directory":
    st.header("College Directory")
    directory={"HODs":[{"Name":"Dr. Rajesh Kumar","Department":"IT","Room":"HOD Office","Contact":"raj@college.edu"}],
               "Faculty":[{"Name":"Prof. Suresh","Department":"IT","Room":"A102","Contact":"suresh@college.edu"}],
               "Transport":[{"Name":"Mr. Ravi","Role":"Bus Coordinator","Contact":"ravi@college.edu"}]}
    search = st.text_input("Search by name or department")
    category = st.selectbox("Select Category", directory.keys())
    col1,col2=st.columns(2)
    for idx,person in enumerate(directory[category]):
        if search.lower() not in person['Name'].lower() and search.lower() not in person.get("Department","").lower(): continue
        col=col1 if idx%2==0 else col2
        with col:
            display_card(person['Name'],f"Dept/Role: {person.get('Department',person.get('Role','N/A'))}\nRoom: {person.get('Room','N/A')}\nContact: {person['Contact']}",color="#a1caff")

# --- STARTUP & PROJECTS HUB PAGE ---
elif option=="Startup & Projects Hub":
    st.header("Startup & Projects Hub")
    projects=[{"Title":"Video Surveillance","Category":"Project","Team":"A","Status":"Completed"},
              {"Title":"Academic Appraisal","Category":"Project","Team":"B","Status":"Sponsored"},
              {"Title":"College Social App","Category":"Startup","Team":"C","Status":"Seeking Mentorship"}]
    search_proj=st.text_input("Search projects by title or team")
    with st.expander("Add New Project / Startup"):
        title=st.text_input("Title"); category=st.selectbox("Category",["Startup","Project","Research"])
        team=st.text_input("Team Members"); status=st.selectbox("Status",["Open","Completed","Seeking Mentorship","Sponsored"])
        description=st.text_area("Description")
        if st.button("Add Project"): projects.append({"Title":title,"Category":category,"Team":team,"Status":status,"Description":description}); st.success(f"{title} added!")
    col1,col2=st.columns(2)
    for idx,proj in enumerate(projects):
        if search_proj.lower() not in proj['Title'].lower() and search_proj.lower() not in proj.get("Team","").lower(): continue
        col=col1 if idx%2==0 else col2
        badge_color={"Completed":"✔️","Sponsored":"💰","Seeking Mentorship":"🧑‍🏫","Open":"🟢"}.get(proj['Status'],"")
        with col:
            display_card(proj['Title'],f"Category: {proj['Category']}\nTeam: {proj.get('Team','N/A')}\nStatus: {proj['Status']}\nDescription: {proj.get('Description','')}",color="#d4f4dd",badge=badge_color)

# --- REPORT ISSUE PAGE ---
elif option=="Report an Issue":
    st.header("Report a College Issue / Maintenance")
    issue_title=st.text_input("Issue Title")
    issue_desc=st.text_area("Description")
    category=st.selectbox("Category",["Facilities","Classroom","Lab","Other"])
    uploaded_image=st.file_uploader("Upload photo",type=["jpg","png","jpeg"])
    if st.button("Submit Issue") and issue_title.strip()!="" and issue_desc.strip()!="":
        display_card(issue_title,f"Description: {issue_desc}\nCategory: {category}",color="#ff6b6b",badge="⚠️")
        if uploaded_image: st.image(uploaded_image, caption="Uploaded Photo", use_column_width=True)
        st.info("Maintenance team will review soon.")
