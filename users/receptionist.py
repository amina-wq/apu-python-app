from utils import logout
from constants import STUDENT
from database import (
    update_profile,
    register_user,
    delete_user,
    users,
    save_users,
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
    print("\n".join(menu))
    choice = input("Enter your choice: ")
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
        subjects = input("Enter subjects(separated by comma, up to 3): ")
        monthly_fee = input("Enter the monthly fee: ")
        register_user(
            name,
            password,
            email,
            STUDENT,
            nationality=nationality,
            passport_no=passport,
            contact_number=contact_number,
            address=address,
            guardian_name=guardian_name,
            guardian_contact=guardian_contact,
            level=level,
            intake=intake,
            subjects=subjects.split(","),
            monthly_fee=monthly_fee,
            payment_status=False,
            completed_studies=False,
        )
        print("The user registered successfully")
    elif choice == "2":
        student_email = input("Enter student email: ")
        update_profile(
            user,
            [
                "nationality",
                "passport_no",
                "contact_number",
                "address",
                "guardian_name",
                "guardian_contact",
                "level",
                "intake",
                "subjects",
                "monthly_fee",
                "payment_status",
                "completed_studies",
            ],
            student_email,
        )
    elif choice == "3":
        student_email = input("Enter student email: ")
        update_student_enrollment(user, student_email)
    elif choice == "4":
        email = input("Enter the e-mail of the student: ")
        delete_user(user, email)
        print("Student record has been deleted!")
    elif choice == "5":
        email = input("Enter the e-mail of the student: ")
        accept_payment(email)
    elif choice == "6":
        return


def update_student_enrollment(user, email):
    student = get_user_by_email(user, email, role=STUDENT)
    print(f'Current subjects of the student: {student["subjects"]}')
    subject_to_be_updated = input(
        "Enter the subject to be replaced"
        "(if more then 1,then separate by comma, up to 3): "
    ).split(",")[:3]
    updated_subject = input(
        "Enter the subject that is to replace"
        "(if more then 1,then separate by comma, up to 3): "
    ).split(",")[:3]
    subject_set = set(student.get("subjects"))
    subject_to_be_updated_set = set(subject_to_be_updated)
    if subject_to_be_updated_set.issubset(subject_set):
        student["subjects"] = (
            list(subject_set - subject_to_be_updated_set) + updated_subject
        )

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
        iter(
            [
                user
                for user in users
                if user["email"] == email and user["role"] == STUDENT
            ]
        ),
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

        save_users()
    else:
        print("This user already paid")


def receptionist_menu(user):
    while True:
        menu = [
            "1. Manage Student",
            "2. Update profile",
            "3. Logout",
        ]
        print("\n".join(menu))
        choice = input("Enter your choice: ")

        if choice == "1":
            manage_student(user)
        elif choice == "2":
            try:
                update_profile(user)
            except Exception:
                continue
        elif choice == "3":
            return logout(user)
        else:
            raise Exception("Invalid choice. Try again")
