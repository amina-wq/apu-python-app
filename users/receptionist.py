import database

from utils import logout
from constants import STUDENT
from database import (
    update_profile,
    register_user,
    delete_user,
    users,
    classes,
    requests,
    save,
    get_user_by_email,
)
from datetime import datetime


def manage_student(user):
    menu = [
        "1. Register Student",
        "2. Update Student Information",
        "3. Update Student Enrollment",
        "4. Delete Student",
        "5. Accept Payment",
        "6. Main menu",
    ]

    while True:
        print("\n".join(menu))
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                name = input("Enter Name: ")
                email = input("Enter Email: ")
                password = input("Enter password: ")
                nationality = input("Enter Nationality: ")
                passport = input("Enter Passport No/IC: ")
                contact_number = input("Enter Contact No: ")
                address = input("Enter Address: ")
                guardian_name = input("Enter Guardian Name: ")
                guardian_contact = input("Enter Guardian Contact No: ")
                level = input("Enter Level: ")
                intake = input("Enter Intake Month/Year: ")
                subjects = input("Enter subjects(separated by comma, up to 3): ").split(",")

                fees = 0
                for _class in classes:
                    if _class["name"] in subjects:
                        fees += int(_class.get("charge", 0))

                register_user(
                    name,
                    password,
                    email,
                    contact_number,
                    STUDENT,
                    nationality=nationality,
                    passport_no=passport,
                    address=address,
                    guardian_name=guardian_name,
                    guardian_contact=guardian_contact,
                    level=level,
                    intake=intake,
                    subjects=subjects,
                    monthly_fee=fees,
                    payment_status=False,
                    completed_studies=False,
                )
            elif choice == "2":
                student_email = input("Enter student email: ")
                if student := get_user_by_email(user, student_email, STUDENT):
                    update_profile(
                        student,
                        [
                            "nationality",
                            "passport_no",
                            "contact_number",
                            "address",
                            "guardian_name",
                            "guardian_contact",
                            "level",
                            "intake",
                            "monthly_fee",
                            "completed_studies",
                        ],
                    )
                else:
                    print("Tutor with this email doesn't exist")
                    continue
            elif choice == "3":
                header = (
                    "Email                    "
                    "| Name            "
                    "| Subject to be replaced "
                    "| Subject that is to replace"
                )
                print(header)
                print("-" * len(header))
                for request in requests:
                    print(
                        f"{request['email']:<25}"
                        f"| {request['nickname']:<15} "
                        f"| {request['from_subject']:<22} "
                        f"| {request['to_subject']:<22}"
                    )
                student_email = input("Enter student email: ")
                student = get_user_by_email(user, student_email, STUDENT)
                if not student:
                    print("No such student found")
                if request := next(iter([request for request in requests if request["email"] == student["email"]])):
                    update_student_enrollment(student)
                    requests.remove(request)
                    database.requests = save("./database/requests.txt", requests)
                else:
                    print("No such request found")
            elif choice == "4":
                email = input("Enter the e-mail of the student: ")
                delete_user(user, email)
            elif choice == "5":
                email = input("Enter the e-mail of the student: ")
                accept_payment(email)
            elif choice == "6":
                return
            else:
                print("Invalid choice. Try again")
        except Exception:
            print("Something went wrong, please try again")
            continue


def update_student_enrollment(student):
    print(f'Current subjects of the student: {", ".join(student["subjects"])}')
    subject_to_be_updated = input(
        "Enter the subject to be replaced" "(if more then 1,then separate by comma, up to 3): "
    ).split(",")[:3]
    updated_subject = input(
        "Enter the subject that is to replace" "(if more then 1,then separate by comma, up to 3): "
    ).split(",")[:3]
    subject_set = set(student.get("subjects"))
    subject_to_be_updated_set = set(subject_to_be_updated)
    if subject_to_be_updated_set.issubset(subject_set):
        student["subjects"] = list(subject_set - subject_to_be_updated_set) + updated_subject

        fees = 0
        for _class in classes:
            if _class["name"] in student["subjects"]:
                fees += int(_class.get("charge", 0))
        student["monthly_fee"] = fees

        database.users = save("./database/users.txt", users, need_backup=True)
        print("Update was successful! ")
    else:
        print(
            "Subject not found "
            "or the student has not registered for any subject yet. "
            "Update Failed. "
            "\nTry again!"
        )


def accept_payment(email):
    user = next(
        iter([user for user in users if user["email"] == email and user["role"] == STUDENT]),
        None,
    )
    if not user:
        print("This user is not a student")
        return
    if not user["payment_status"]:
        user["payment_status"] = True
        print(
            f"OFFICIAL RECEIPT\n"
            f'Received From: {user["nickname"]}\n'
            f'The sum of {user["monthly_fee"]}\n'
            f"Date: {datetime.now()}"
        )
        database.users = save("./database/users.txt", users, need_backup=True)
        input("Press 'Enter' key to continue...")
    else:
        print("This user already paid")


def receptionist_menu(user):
    """Receptionist menu"""
    menu = [
        "1. Manage Student",
        "2. Update profile",
        "3. Logout",
    ]

    while True:
        print("\n".join(menu))
        choice = input("Enter your choice: ")
        try:
            if choice == "1":
                manage_student(user)
            elif choice == "2":
                update_profile(user)
            elif choice == "3":
                return logout(user)
            else:
                print("Invalid choice. Try again")
        except Exception:
            print("Something went wrong, please try again")
            continue
