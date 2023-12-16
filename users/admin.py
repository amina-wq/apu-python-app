from utils import logout
from database import register_user, delete_user, update_profile, users
from constants import RECEPTIONIST, STUDENT


def manage_receptionists(user):
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
        print("The user registered successfully")
    elif choice == "2":
        email = input("Enter the employees email: ")
        delete_user(user, email)
    elif choice == "3":
        return
    else:
        raise Exception("Invalid choice. Try again")


def manage_tutor(user):
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
        classes = input("Enter employee classes separated by ',': ").split(",")
        salary = input("Enter employees salary: ")
        register_user(
            name,
            password,
            email,
            RECEPTIONIST,
            classes=classes,
            salary=salary,
        )
        print("The user registered successfully")
    elif choice == "2":
        email = input("Enter the employees email: ")
        delete_user(user, email)
    elif choice == "3":
        return
    else:
        raise Exception("Invalid choice. Try again")


def view_monthly_income():
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


def admin_menu(user):
    menu = [
        "1. Register/Delete Tutors",
        "2. Register/Delete Receptionists",
        "3. View Monthly Income Report",
        "4. Update profile",
        "5. Logout",
    ]

    while True:
        print("\n".join(menu))
        choice = input("Enter your choice: ")
        if choice == "1":
            manage_tutor(user)
        elif choice == "2":
            manage_receptionists(user)
        elif choice == "3":
            view_monthly_income()
        elif choice == "4":
            try:
                update_profile(user)
            except Exception:
                continue
        elif choice == "5":
            return logout(user)
        else:
            raise Exception("Invalid choice. Try again")
