# 🦷 JJ Dental Clinic Management System

A Python-based dental clinic management system with both a **command-line interface** and a **Streamlit web app**. Built using Object-Oriented Programming (OOP) principles, it allows clinic staff to manage patient records and send automated WhatsApp appointment reminders.

---

## ✨ Features

- **Add & Edit Patients** — Register new patients or update existing records with full medical history
- **View Patients** — Browse and search patient records by name or ID
- **Medical History Questionnaire** — Structured Q&A form covering allergies, medications, anesthesia reactions, and past procedures
- **Treatment Tracking** — Select from 10+ predefined dental treatments or enter a custom one
- **Appointment Reminders** — Automatically sends WhatsApp messages to patients whose next visit is within 2 days
- **Delete Patient** — Remove records with automatic patient ID reassignment
- **Duplicate Detection** — Prevents identical records from being added twice
- **Persistent Storage** — All data is saved locally in a `patients.json` file

---

## 🗂️ Project Structure

```
jj-dental-clinic-management-system/
│
├── OOPproject.py       # Core OOP logic (Patient, PatientDatabase, PatientManager, ReminderService, JJClinicApp)
├── app.py              # Streamlit web app interface
├── patients.json       # Local JSON database (auto-created on first run)
└── README.md
```

---

## 🏗️ OOP Design

The project is structured around four main classes:

| Class | Responsibility |
|---|---|
| `Patient` | Encapsulates a single patient's data with getters/setters |
| `PatientDatabase` | Handles loading, saving, adding, updating, and deleting patients from JSON |
| `PatientManager` | Manages business logic — validation, add/edit/delete/show operations |
| `ReminderService` | Sends WhatsApp reminders via `pywhatkit` for upcoming appointments |
| `JJClinicApp` | CLI entry point that ties everything together |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Google Chrome (required by `pywhatkit` for WhatsApp Web)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/jj-dental-clinic-management-system.git
   cd jj-dental-clinic-management-system
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit pywhatkit
   ```

### Running the App

**Web App (Streamlit):**
```bash
streamlit run app.py
```

**Command-Line Interface:**
```bash
python OOPproject.py
```

---

## 📋 How to Use

### Web App
1. Launch with `streamlit run app.py`
2. Use the navigation buttons at the top to switch between sections:
   - **Add/Edit Patient** — Select an existing patient to edit, or fill in the form to add a new one
   - **View Patients** — Search and browse all records; see how many days until each patient's next visit
   - **Send Reminders** — Trigger WhatsApp reminders for patients with appointments in the next 2 days
   - **Delete Patient** — Select and remove a patient record

### CLI
Run `python OOPproject.py` and follow the on-screen menu:
```
=== JJ Dental Clinic ===
1. Add or Edit Patient
2. Show All Patients
3. Send WhatsApp Reminders
4. Delete Patient Record
5. Exit
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web app UI |
| `pywhatkit` | Sending WhatsApp messages via WhatsApp Web |
| `json` | Local data persistence (built-in) |
| `datetime` | Date validation and appointment logic (built-in) |

---

## ⚠️ Notes

- **WhatsApp reminders** require WhatsApp Web to be logged in on your default browser. The `pywhatkit` library opens the browser automatically.
- The `patients.json` file is created automatically in the project directory on first run.
- Patient IDs are auto-generated (e.g., `P001`, `P002`) and reassigned when a record is deleted.

---

## 👩‍💻 Authors

Developed as an Object-Oriented Programming course project.
