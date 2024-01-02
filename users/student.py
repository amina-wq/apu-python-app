from database import update_profile
from utils import logout

def read_student_records():
    try:
        with open('student_records.txt', 'r') as file:
            records = [line.strip().split(',') for line in file.readlines()]
            student_records = {int(record[0]): record[1:] for record in records}
            return student_records
    except FileNotFoundError:
        return {}


def write_student_records(student_records):
    with open('student_records.txt', 'w') as file:
        for student_id, details in student_records.items():
            record = ','.join([str(student_id)] + details)
            file.write(record + '\n')


def view_profile(student_id, student_records):
    if student_id in student_records:
        print("Student Profile:")
        print(f"ID: {student_id}")
        print(f"Name: {student_records[student_id][0]}")
        print(f"Schedule: {student_records[student_id][1]}")
        print(f"Enrolled Subjects: {student_records[student_id][2]}")
        print(f"Pending Requests: {student_records[student_id][3]}")
        print(f"Payment Status: {student_records[student_id][4]}")
    else:
        print("Student ID not found!")


def send_request(student_id, request, student_records):
    if student_id in student_records:
        pending_requests = student_records[student_id][3]
        updated_requests = pending_requests + ', ' + request if pending_requests else request
        student_records[student_id][3] = updated_requests
        write_student_records(student_records)
        print("Request sent successfully!")
    else:
        print("Student ID not found!")


def delete_pending_request(student_id, student_records):
    if student_id in student_records:
        student_records[student_id][3] = ""
        write_student_records(student_records)
        print("Pending request deleted successfully!")
    else:
        print("Student ID not found!")


def view_payment_status(student_id, student_records):
    if student_id in student_records:
        print(f"Payment status: {student_records[student_id][4]}")
    else:
        print("Student ID not found!")

# Function to get student ID from user input
def get_student_id():
    while True:
        try:
            student_id = int(input("Enter your ID: "))
            return student_id
        except ValueError:
            print("Please enter a valid ID (a number).")

# Menu
def menu(student_id, student_records):
    while True:
        print("\nMenu:")
        print("1. View Profile")
        print("2. Send Request to Change Enrolled Subjects")
        print("3. View Payment Status")
        print("4. Delete Pending Requests")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            view_profile(student_id, student_records)
        elif choice == '2':
            request = input("Enter your request: ")
            send_request(student_id, request, student_records)
        elif choice == '3':
            view_payment_status(student_id, student_records)
        elif choice == '4':
            delete_pending_request(student_id, student_records)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# Example usage
student_records = read_student_records()
student_id = get_student_id()
menu(student_id, student_records)

