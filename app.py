import streamlit as st
from OOPproject import PatientDatabase, PatientManager, ReminderService
from datetime import datetime

# Initialize session state
if 'db' not in st.session_state:
    st.session_state.db = PatientDatabase()
if 'manager' not in st.session_state:
    st.session_state.manager = PatientManager(st.session_state.db)
if 'reminder_service' not in st.session_state:
    st.session_state.reminder_service = ReminderService(st.session_state.db)

# Page configuration
st.set_page_config(
    page_title="JJ Dental Clinic",
    page_icon="🦷",
    layout="wide"
)


# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #ffe6f0; /* light pink background */
    }
    .stButton>button {
        background-color: #d72660; /* dark pink */
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        transition: background-color 0.2s, color 0.2s;
    }
    .stButton>button:hover {
        background-color: white;
        color: #d72660;
        border: 1px solid #d72660;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 5px;
        background-color: #fff0f6; /* very light pink */
    }
    .patient-card {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(215,38,96,0.08);
    }
    .header {
        color: #d72660; /* dark pink for headers */
    }
    </style>
    """, unsafe_allow_html=True)

# Main App
def main():
    st.title("🦷 JJ Dental Clinic Management System")
    st.markdown("---")

    # Center the navigation buttons using empty columns as spacers
    spacer1, col1, col2, col3, col4, spacer2 = st.columns([1, 2, 2, 2, 2, 1])

    # Use session_state to persist selected page
    if "page" not in st.session_state:
        st.session_state.page = "Add/Edit Patient"

    with col1:
        if st.button("Add/Edit Patient"):
            st.session_state.page = "Add/Edit Patient"
    with col2:
        if st.button("View Patients"):
            st.session_state.page = "View Patients"
    with col3:
        if st.button("Send Reminders"):
            st.session_state.page = "Send Reminders"
    with col4:
        if st.button("Delete Patient"):
            st.session_state.page = "Delete Patient"

    page = st.session_state.page

    if page == "Add/Edit Patient":
        add_edit_patient()
    elif page == "View Patients":
        view_patients()
    elif page == "Send Reminders":
        send_reminders()
    elif page == "Delete Patient":
        delete_patient()

def add_edit_patient():
    st.header("Add or Edit Patient Record")
    
    data = st.session_state.db.get_all_patients()
    existing_ids = [p["patient_id"] for p in data]
    
    col1, col2 = st.columns(2)
    
    with col1:
        existing_id = st.selectbox("Select patient to edit (or leave as 'New Patient' to add new)", 
                                 ["New Patient"] + existing_ids)
    
    if existing_id != "New Patient":
        patient = next((p for p in data if p["patient_id"] == existing_id), None)
        if patient:
            with st.expander("Current Patient Details"):
                st.json(patient)
            
            name = st.text_input("Name", value=patient["name"]).title()
            contact = st.text_input("Contact Number (11 digits)", value=patient["contact"])
            date = st.text_input("Date (YYYY-MM-DD)", value=patient["date"])
            st.subheader("Medical History Questionnaire")
            st.markdown("Please answer the following questions to update the patient's medical history:")
            # Pre-fill the medical history questions with existing answers
            existing_history = patient.get("history", "")
            existing_answers = existing_history.split("\n") if existing_history else []

            questions = [
                "Does the patient have any known allergies or medical conditions?",
                "Is the patient currently taking any medications?",
                "Has the patient ever had a reaction to local anesthesia or antibiotics?",
                "Has the patient undergone any major dental procedures in the past?",
                "Any other relevant medical history or concerns?"
            ]

            responses = []
            for i, question in enumerate(questions):
                default_answer = "No"
                default_detail = ""

                if i < len(existing_answers):
                    if "Yes" in existing_answers[i]:
                        default_answer = "Yes"
                        parts = existing_answers[i].split("Details:")
                        if len(parts) > 1:
                            default_detail = parts[1].strip()

                col1, col2 = st.columns([3, 2])
                with col1:
                    response = st.radio(f"{question}", key=f"edit_q_{i}", options=["Yes", "No"], index=0 if default_answer == "Yes" else 1, horizontal=True)
                if response == "Yes":
                    with col2:
                        detail = st.text_input("Please specify:", value=default_detail, key=f"edit_q_detail_{i}")
                    responses.append(f"{question} - Yes. Details: {detail}")
                else:
                    responses.append(f"{question} - No.")

            history = "\n".join(responses)

            
            treatments = [
                "Dental Cleaning", "Cavity Filling", "Tooth Extraction", "Root Canal",
                "Dental Crown", "Dental Bridge", "Dentures", "Teeth Whitening",
                "Braces", "X-rays", "Other"
            ]
            
            treatment_index = treatments.index(patient["treatment"]) if patient["treatment"] in treatments else len(treatments)-1
            treatment_choice = st.selectbox("Treatment", treatments, index=treatment_index)
            
            if treatment_choice == "Other":
                treatment = st.text_input("Enter treatment name")
            else:
                treatment = treatment_choice
                
            next_visit = st.text_input("Next Visit Date (YYYY-MM-DD)", value=patient["next_visit"])
            
            if st.button("Update Patient"):
                if (st.session_state.manager.is_valid_name(name) and 
                    st.session_state.manager.is_valid_contact(contact) and 
                    st.session_state.manager.is_valid_date(date) and 
                    st.session_state.manager.is_valid_date(next_visit)):
                    
                    patient.update({
                        "name": name,
                        "contact": contact,
                        "date": date,
                        "history": history,
                        "treatment": treatment,
                        "next_visit": next_visit
                    })
                    
                    st.session_state.db.save_data()
                    st.success("Patient record updated successfully!")
                else:
                    st.error("Please check your inputs. Some fields are invalid.")
    else:
        with col2:
            st.info("Enter new patient details below")
        
        name = st.text_input("Name").title()
        contact = st.text_input("Contact Number (11 digits)")
        date = st.text_input("Date (YYYY-MM-DD)")
        st.subheader("Medical History Questionnaire")
        questions = [
            "Does the patient have any known allergies or medical conditions?",
            "Is the patient currently taking any medications?",
            "Has the patient ever had a reaction to local anesthesia or antibiotics?",
            "Has the patient undergone any major dental procedures in the past?",
            "Any other relevant medical history or concerns?"
        ]

        responses = []
        for i, question in enumerate(questions):
            col1, col2 = st.columns([3, 2])
            with col1:
                response = st.radio(f"{question}", key=f"q_{i}", options=["Yes", "No"], horizontal=True)
            if response == "Yes":
                with col2:
                    detail = st.text_input("Please specify:", key=f"q_detail_{i}")
                responses.append(f"{question} - Yes. Details: {detail}")
            else:
                responses.append(f"{question} - No.")

        history = "\n".join(responses)

        
        treatments = [
            "Dental Cleaning", "Cavity Filling", "Tooth Extraction", "Root Canal",
            "Dental Crown", "Dental Bridge", "Dentures", "Teeth Whitening",
            "Braces", "X-rays", "Other"
        ]
        
        treatment_choice = st.selectbox("Treatment", treatments)
        
        if treatment_choice == "Other":
            treatment = st.text_input("Enter treatment name")
        else:
            treatment = treatment_choice
            
        next_visit = st.text_input("Next Visit Date (YYYY-MM-DD)")
        
        if st.button("Add Patient"):
            if (st.session_state.manager.is_valid_name(name) and 
                st.session_state.manager.is_valid_contact(contact) and 
                st.session_state.manager.is_valid_date(date) and 
                st.session_state.manager.is_valid_date(next_visit)):
                
                patient_id = st.session_state.db.generate_patient_id()
                new_patient = {
                    "patient_id": patient_id,
                    "name": name,
                    "contact": contact,
                    "date": date,
                    "history": history,
                    "treatment": treatment,
                    "next_visit": next_visit
                }
                
                # Check for duplicates
                duplicate = False
                for p in data:
                    if (p['name'].lower() == name.lower() and
                        p['contact'] == contact and
                        p['date'] == date and
                        p['history'].lower() == history.lower() and
                        p['treatment'].lower() == treatment.lower() and
                        p['next_visit'] == next_visit):
                        duplicate = True
                        break
                
                if not duplicate:
                    st.session_state.db.add_patient(new_patient)
                    st.success("New patient added successfully!")
                    st.balloons()
                else:
                    st.warning("This patient record already exists.")
            else:
                st.error("Please check your inputs. Some fields are invalid.")

def view_patients():
    st.header("Patient Records")
    
    data = st.session_state.db.get_all_patients()
    if not data:
        st.warning("No patient records found.")
        return
    
    search_term = st.text_input("Search by name or ID")
    
    if search_term:
        filtered_data = [
            p for p in data 
            if search_term.lower() in p["name"].lower() or 
            search_term.upper() in p["patient_id"].upper()
        ]
    else:
        filtered_data = data
    
    for patient in filtered_data:
        with st.expander(f"{patient['name']} (ID: {patient['patient_id']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Contact:** {patient['contact']}")
                st.markdown(f"**Visit Date:** {patient['date']}")
                st.markdown(f"**Next Visit:** {patient['next_visit']}")
                
            with col2:
                st.markdown(f"**Treatment:** {patient['treatment']}")
                st.markdown("**Medical History:**")
                st.write(patient['history'])
            
            # Show days until next visit
            try:
                visit_date = datetime.strptime(patient["next_visit"], "%Y-%m-%d").date()
                today = datetime.today().date()
                days_left = (visit_date - today).days
                
                if days_left < 0:
                    st.warning(f"Appointment was {abs(days_left)} days ago")
                elif days_left == 0:
                    st.success("Appointment is today!")
                else:
                    st.info(f"Appointment in {days_left} days")
            except:
                pass

def send_reminders():
    st.header("Send WhatsApp Reminders")
    
    if st.button("Check and Send Reminders"):
        with st.spinner("Sending reminders..."):
            st.session_state.reminder_service.send_reminders()
        st.success("Reminder process completed!")

def delete_patient():
    st.header("Delete Patient Record")
    
    data = st.session_state.db.get_all_patients()
    if not data:
        st.warning("No patient records to delete.")
        return
    
    patient_options = [f"{p['name']} ({p['patient_id']})" for p in data]
    selected_patient = st.selectbox("Select patient to delete", patient_options)
    
    if selected_patient:
        patient_id = selected_patient.split("(")[1].replace(")", "")
        
        if st.button("Delete Patient", key="delete_button"):
            for i, patient in enumerate(data):
                if patient["patient_id"] == patient_id:
                    st.session_state.db.delete_patient(i)
                    st.success(f"Patient {selected_patient} deleted successfully!")
                    break

if __name__ == "__main__":
    main()