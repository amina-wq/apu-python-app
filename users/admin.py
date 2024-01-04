from utils import logout
from database import register_user, delete_user, update_profile, users
from constants import RECEPTIONIST, STUDENT, TUTOR


def manage_receptionists(user):
    """Creates and Deletes Receptionist"""
    menu = [
        "1. Register Receptionist",
        "2. Delete Receptionist",
        "3. Main menu",
    ]
    print("\n".join(menu))
    choice = input("Enter your choice: ")
    if choice == "1":
        name = input("Enter employees name: ")
        password = input("Set employees password: ")
        email = input("Enter employees email: ")
        salary = input("Enter employees salary: ")
        register_user(
            name,
            password,
            email,
            RECEPTIONIST,
            salary=salary,
        )
    elif choice == "2":
        email = input("Enter the employees email: ")
        delete_user(user, email)
    elif choice == "3":
        return
    else:
        raise Exception("Invalid choice. Try again")


def manage_tutor(user):
    """Creates and Deletes Tutor"""
    menu = [
        "1. Register Tutor",
        "2. Delete Tutor",
        "3. Main menu",
    ]
    print("\n".join(menu))
    choice = input("Enter your choice: ")
    if choice == "1":
        name = input("Enter employees name: ")
        password = input("Set employees password: ")
        email = input("Enter employees email: ")
        salary = input("Enter employees salary: ")
        register_user(
            name,
            password,
            email,
            TUTOR,
            classes="",
            salary=salary,
        )
    elif choice == "2":
        email = input("Enter the employees email: ")
        delete_user(user, email)
    elif choice == "3":
        return
    else:
        raise ValueError("Invalid choice. Try again")


def view_monthly_income():
    """Monthly income calculation"""
    income = 0
    for user in users:
        if user["role"] == STUDENT:
            if user["payment_status"]:
                status = "Paid"
                income += int(user["monthly_fee"])
            else:
                status = "Pending"
            print(
                f"Name: {user['nickname']}, "
                f"Role: {user['role']}, "
                f"Fee: {user['monthly_fee']}, "
                f"Status: {status}"
            )
        else:
            income -= int(user["salary"])
            print(
                f"Name: {user['nickname']}, "
                f"Role: {user['role']}, "
                f"Salary: {user['salary']} "
            )
    print(f"Monthly income: {income}")
    input("Press 'Enter' key to continue...")


def admin_menu(user):
    """Administrator menu"""
    menu = [
        "1. Manage Tutors",
        "2. Manage Receptionists",
        "3. View Monthly Income Report",
        "4. Update profile",
        "5. Logout",
    ]

    while True:
        print("\n".join(menu))
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                manage_tutor(user)
            elif choice == "2":
                manage_receptionists(user)
            elif choice == "3":
                view_monthly_income()
            elif choice == "4":
                update_profile(user)
            elif choice == "5":
                return logout(user)
            else:
                raise ValueError("Invalid choice. Try again")
        except Exception:
            print("Something went wrong, please try again")
            continue
