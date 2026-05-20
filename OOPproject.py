import json
import time
from datetime import datetime
import pywhatkit as pwk

DATA_FILE = 'patients.json'

# Represents a single patient record
class Patient:
    def __init__(self, patient_id, name, contact, date, history, treatment, next_visit):
        self.__patient_id = patient_id
        self.__name = name
        self.__contact = contact
        self.__date = date
        self.__history = history
        self.__treatment = treatment
        self.__next_visit = next_visit

    # accessors
    def get_patient_id(self):
        return self.__patient_id

    def get_name(self):
        return self.__name

    def get_contact(self):
        return self.__contact

    def get_date(self):
        return self.__date

    def get_history(self):
        return self.__history

    def get_treatment(self):
        return self.__treatment

    def get_next_visit(self):
        return self.__next_visit

    # mutators
    def set_patient_id(self, value):
        self.__patient_id = value

    def set_name(self, value):
        self.__name = value

    def set_contact(self, value):
        self.__contact = value

    def set_date(self, value):
        self.__date = value

    def set_history(self, value):
        self.__history = value

    def set_treatment(self, value):
        self.__treatment = value

    def set_next_visit(self, value):
        self.__next_visit = value

    # Convert to dictionary (still needed for JSON storage)
    def to_dict(self):
        return {
            "patient_id": self.__patient_id,
            "name": self.__name,
            "contact": self.__contact,
            "date": self.__date,
            "history": self.__history,
            "treatment": self.__treatment,
            "next_visit": self.__next_visit
        }

# Handles loading/saving patient data
class PatientDatabase:
    def __init__(self, filename=DATA_FILE):
        self.__filename = filename
        self.__patients = self.load_data()

    # Getter for filename
    def get_filename(self):
        return self.__filename

    # Setter for filename
    def set_filename(self, new_filename):
        self.__filename = new_filename

    # Getter for patients list
    def get_all_patients(self):
        return self.__patients

    # Set the entire patient list (used carefully)
    def set_all_patients(self, new_list):
        self.__patients = new_list

    # Load patients from JSON file
    def load_data(self):
        try:
            with open(self.__filename, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        return data

    # Save patients to JSON file
    def save_data(self):
        with open(self.__filename, 'w') as file:
            json.dump(self.__patients, file, indent=4)

    # Add a new patient dictionary
    def add_patient(self, patient_dict):
        self.__patients.append(patient_dict)
        self.save_data()

    # Update a patient at a specific index
    def update_patient(self, index, new_data):
        self.__patients[index] = new_data
        self.save_data()

    # Delete a patient and reassign IDs
    def delete_patient(self, index):
        del self.__patients[index]
        for i in range(index, len(self.__patients)):
            old_id_num = int(self.__patients[i]["patient_id"][1:])
            new_id_num = old_id_num - 1
            self.__patients[i]["patient_id"] = f'P{new_id_num:03d}'
        self.save_data()

    # Generate next patient ID
    def generate_patient_id(self):
        if len(self.__patients) == 0:
            return "P001"
        numbers = [int(p["patient_id"][1:]) for p in self.__patients]
        next_number = max(numbers) + 1
        return f"P{next_number:03d}"


# Manages patient-related operations (Add, Edit, Delete, Show)
class PatientManager:
    def __init__(self, db):
        self.__db = db  # private attribute

    # Getter for db
    def get_db(self):
        return self.__db

    # Setter for db
    def set_db(self, new_db):
        self.__db = new_db

    def is_valid_name(self, text):
        text = text.strip()  # Remove spaces at start/end
        if not text:
            return False  # Name can't be empty
        for char in text:
            if not (char.isalpha() or char.isspace()):
                return False  # Only allow letters and spaces
        return True

    def is_valid_contact(self, contact):
        # Remove spaces
        contact = contact.strip()
        # Check if all characters are digits and length is 11
        if contact.isdigit() and len(contact) == 11:
            return True
        return False

    def is_valid_date(self, date_str):
        # Remove spaces
        date_str = date_str.strip()
        if len(date_str) != 10:   # Check length
            return False
        
        # Split by '-'
        parts = date_str.split('-')
        if len(parts) != 3:
            return False
        
        year, month, day = parts
        # Check if year, month, day are digits
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return False
        
        year = int(year)
        month = int(month)
        day = int(day)
        if year < 1900 or month < 1 or month > 12 or day < 1 or day > 31: # Check valid ranges
            return False
        
        # Check for months with less than 31 days
        if month in [4, 6, 9, 11] and day > 30:
            return False
        
        # February check (ignoring leap years)
        if month == 2 and day > 29:
            return False
        return True

    def collect_patient_history(self):
        questions = [
            "Does the patient have any known allergies or medical conditions?",
            "Is the patient currently taking any medications?",
            "Has the patient ever had a reaction to local anesthesia or antibiotics?",
            "Has the patient undergone any major dental procedures in the past?",
            "Any Other relevant medical history or concerns?"
        ]

        responses = []
        for q in questions:
            while True:
                answer = input(f"{q} (yes/no): ").strip().lower()
                if answer in ["yes", "no"]:
                    break
                print("Please answer with 'yes' or 'no'.")
            
            if answer == "yes":
                detail = input("Please specify: ").strip()
                responses.append(f"{q} - Yes. Details: {detail}")
            else:
                responses.append(f"{q} - No.")

        return "\n".join(responses)


    def add_or_edit_patient(self):
        data = self.__db.get_all_patients()

        print("\n--- Add or Edit Patient ---")
        existing_id = input("Enter patient ID to edit (or press Enter to add new): ").strip().upper()

        # Edit existing record if ID is entered
        if existing_id:
            for patient in data:
                if patient["patient_id"] == existing_id:
                    print("\nExisting patient record found:")
                    print(json.dumps(patient, indent=4))
                    print("\nEnter new details (press Enter to keep existing values):")

                    new_name = input(f"Enter patient name [{patient['name']}]: ").strip()
                    if new_name:
                        if self.is_valid_name(new_name):
                            name = new_name
                        else:
                            print("Invalid name. Keeping old value.")
                            name = patient['name']
                    else:
                        name = patient['name']

                    contact = input(f"Enter contact number [{patient['contact']}]: ").strip()
                    if not self.is_valid_contact(contact):
                        print("Invalid contact number. Keeping old value.")
                        contact = patient['contact']

                    date = input(f"Enter today's date (YYYY-MM-DD) [{patient['date']}]: ").strip()
                    if not self.is_valid_date(date):
                        print("Invalid date. Keeping old value.")
                        date = patient['date']

                    print("\n--- Update Patient History ---")
                    update_history = input("Do you want to update patient history? (yes/no): ").strip().lower()
                    if update_history == "yes":
                        history = self.collect_patient_history()
                    else:
                        history = patient['history']


                    treatments = [
                        "Dental Cleaning", "Cavity Filling", "Tooth Extraction", "Root Canal",
                        "Dental Crown", "Dental Bridge", "Dentures", "Teeth Whitening",
                        "Braces", "X-rays", "Other"
                    ]

                    print("\nAvailable Treatments:")
                    for i, t in enumerate(treatments, start=1):
                        print(f"{i}. {t}")

                    while True:
                        try:
                            choice = input(f"Choose treatment (1-11) [{patient['treatment']}]: ")
                            if choice == "":
                                treatment = patient['treatment']
                                break
                            choice = int(choice)
                            if 1 <= choice <= len(treatments):
                                if treatments[choice - 1] == "Other":
                                    treatment = input("Enter treatment name: ")
                                else:
                                    treatment = treatments[choice - 1]
                                break
                            else:
                                print("Please choose a number between 1 and 11.")
                        except ValueError:
                            print("Invalid input. Enter a number or press Enter.")

                    next_visit = input(f"Enter next visit date (YYYY-MM-DD) [{patient['next_visit']}]: ") or patient['next_visit']

                    patient.update({
                        "name": name,
                        "contact": contact,
                        "date": date,
                        "history": history,
                        "treatment": treatment,
                        "next_visit": next_visit
                    })

                    self.__db.save_data()
                    print("\nPatient record updated successfully!\n")
                    return

            print("No patient found with that ID. Please try again.")
            return

        while True:
            name = input("Enter patient name: ").strip()
            if self.is_valid_name(name): break
            print("Invalid name.")

        while True:
            contact = input("Enter contact number (11 digits): ").strip()
            if self.is_valid_contact(contact): break
            print("Invalid contact.")

        while True:
            date = input("Enter today's date (YYYY-MM-DD): ").strip()
            if self.is_valid_date(date): break
            print("Invalid date.")

        print("\n--- Patient History Questions ---")
        history = self.collect_patient_history()


        treatments = [
            "Dental Cleaning", "Cavity Filling", "Tooth Extraction", "Root Canal",
            "Dental Crown", "Dental Bridge", "Dentures", "Teeth Whitening",
            "Braces", "X-rays", "Other"
        ]
        print("\nAvailable Treatments:")
        for i, t in enumerate(treatments, start=1):
            print(f"{i}. {t}")

        while True:
            try:
                treatment_choice = int(input("Choose treatment (1-11): "))
                if 1 <= treatment_choice <= len(treatments): break
            except: pass

        treatment = input("Enter treatment name: ") if treatments[treatment_choice - 1] == "Other" else treatments[treatment_choice - 1]

        while True:
            next_visit = input("Enter next visit date (YYYY-MM-DD): ").strip()
            if self.is_valid_date(next_visit): break
            print("Invalid next visit date.")

        for patient in data:
            if (
                patient['name'].lower() == name.lower() and
                patient['contact'] == contact and
                patient['date'] == date and
                patient['history'].lower() == history.lower() and
                patient['treatment'].lower() == treatment.lower() and
                patient['next_visit'] == next_visit
            ):
                print("\nPatient data already exists. Duplicate entry not added.\n")
                return

        patient_id = self.__db.generate_patient_id()
        new_patient = Patient(patient_id, name, contact, date, history, treatment, next_visit)
        self.__db.add_patient(new_patient.to_dict())
        print("\nNew patient data saved successfully!\n")

    def show_patients(self):
        data = self.__db.get_all_patients()
        if not data:
            print("No patients found.")
            return
        print("\nList of Patients:\n")
        for p in data:
            print(f"ID: {p['patient_id']}")
            print(f"Name: {p['name']}")
            print(f"Contact: {p['contact']}")
            print(f"Treatment: {p['treatment']}")
            print(f"Next Visit: {p['next_visit']}")
            print("-" * 30)

    def delete_patient(self):
        data = self.__db.get_all_patients()
        if not data:
            print("No patient records to delete.")
            return

        name_to_delete = input("Enter patient name to delete: ").strip().lower()
        id_to_delete = input("Enter patient ID to delete (e.g. P003): ").strip().upper()

        for i, patient in enumerate(data):
            if patient["name"].strip().lower() == name_to_delete and patient["patient_id"] == id_to_delete:
                print(f"\nFound patient: {patient['name']} (ID: {patient['patient_id']}) - Deleting record.")
                self.__db.delete_patient(i)
                print(f"\nPatient '{name_to_delete}' with ID '{id_to_delete}' deleted successfully.\n")
                return
        print("No matching patient found.")

# Sends WhatsApp reminders
class ReminderService:
    def __init__(self, db):
        self.__db = db  # Private attribute

    # Getter for db
    def get_database(self):
        return self.__db

    # Setter for db
    def set_database(self, new_db):
        self.__db = new_db

    def send_reminders(self):
        today = datetime.today().date()
        print("\n Sending WhatsApp reminders...\n")
        for patient in self.__db.get_all_patients():
            try:
                visit_date = datetime.strptime(patient["next_visit"], "%Y-%m-%d").date()
                days_left = (visit_date - today).days
                if 0 <= days_left <= 2:
                    name = patient["name"]
                    contact = patient["contact"]
                    treatment = patient["treatment"]

                    message = f"Your appointment at JJ Dental Clinic for your \"{treatment}\" Treatment is on {visit_date}.\nCall the clinic and confirm your appointment.\nJAZAKALLAH"

                    phone_number = contact if contact.startswith("+") else "+92" + contact.lstrip("0")
                    pwk.sendwhatmsg_instantly(phone_number, message, wait_time=12, tab_close=False)
                    time.sleep(10)
                    print(" Reminder sent to " + name + " (" + phone_number + ")")
            except Exception as e:
                print(" Failed to send reminder to " + patient["name"] + ": " + str(e))

# Main App
class JJClinicApp:
    def __init__(self):
        db = PatientDatabase()
        self.__manager = PatientManager(db)  # Private attribute
        self.__reminder_service = ReminderService(db)  # Private attribute

    # Getter for manager
    def get_manager(self):
        return self.__manager

    # Setter for manager
    def set_manager(self, new_manager):
        self.__manager = new_manager

    # Getter for reminder service
    def get_reminder_service(self):
        return self.__reminder_service

    # Setter for reminder service
    def set_reminder_service(self, new_service):
        self.__reminder_service = new_service

    def run(self):
        while True:
            print("\n=== JJ Dental Clinic ===")
            print("1. Add or Edit Patient")
            print("2. Show All Patients")
            print("3. Send WhatsApp Reminders")
            print("4. Delete Patient Record")
            print("5. Exit")
            choice = input("Choose an option (1-5): ")

            if choice == '1':
                self.__manager.add_or_edit_patient()
            elif choice == '2':
                self.__manager.show_patients()
            elif choice == '3':
                self.__reminder_service.send_reminders()
            elif choice == '4':
                self.__manager.delete_patient()
            elif choice == '5':
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

# Run the program
if __name__ == '__main__':
    app = JJClinicApp()
    app.run()
