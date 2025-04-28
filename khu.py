import hashlib
import datetime
import streamlit as st

# Define the Block structure
class AppointmentBlock:
    def __init__(self, patient_name, doctor_name, appointment_time, previous_hash=''):
        self.patient_name = patient_name
        self.doctor_name = doctor_name
        self.appointment_time = appointment_time
        self.previous_hash = previous_hash
        self.timestamp = str(datetime.datetime.now())
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Combine all the information and hash it
        block_contents = (
            self.patient_name +
            self.doctor_name +
            self.appointment_time +
            self.previous_hash +
            self.timestamp
        )
        return hashlib.sha256(block_contents.encode()).hexdigest()

# Define the Blockchain
class AppointmentBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # First block manually created
        return AppointmentBlock("Genesis Patient", "Genesis Doctor", "2025-01-01 00:00", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_appointment(self, patient_name, doctor_name, appointment_time):
        previous_hash = self.get_latest_block().hash
        new_block = AppointmentBlock(patient_name, doctor_name, appointment_time, previous_hash)
        self.chain.append(new_block)

    def display_chain(self):
        # Prepare chain display in a user-friendly format
        chain_info = []
        for idx, block in enumerate(self.chain):
            block_info = {
                "Block Number": idx,
                "Patient": block.patient_name,
                "Doctor": block.doctor_name,
                "Appointment Time": block.appointment_time,
                "Previous Hash": block.previous_hash,
                "Current Hash": block.hash,
            }
            chain_info.append(block_info)
        return chain_info

# Streamlit UI setup
def display_appointments(appointment_chain):
    chain_info = appointment_chain.display_chain()
    for block in chain_info:
        st.subheader(f"Block {block['Block Number']}")
        st.write(f"**Patient**: {block['Patient']}")
        st.write(f"**Doctor**: {block['Doctor']}")
        st.write(f"**Appointment Time**: {block['Appointment Time']}")
        st.write(f"**Previous Hash**: {block['Previous Hash']}")
        st.write(f"**Current Hash**: {block['Current Hash']}")
        st.markdown("---")

def main():
    st.title("Appointment Blockchain System")
    
    # Initialize blockchain
    appointment_chain = AppointmentBlockchain()
    
    st.header("Add an Appointment")
    
    # User inputs for new appointment
    patient_name = st.text_input("Patient Name")
    doctor_name = st.text_input("Doctor Name")
    appointment_time = st.text_input("Appointment Time (YYYY-MM-DD HH:MM)")

    if st.button("Add Appointment"):
        if patient_name and doctor_name and appointment_time:
            # Add appointment to the blockchain
            appointment_chain.add_appointment(patient_name, doctor_name, appointment_time)
            st.success(f"Appointment for {patient_name} with {doctor_name} added successfully.")
        else:
            st.error("Please fill all the fields.")
    
    # Display the blockchain
    st.header("Appointment Blockchain")
    display_appointments(appointment_chain)

if __name__ == "__main__":
    main()
