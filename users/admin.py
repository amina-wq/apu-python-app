from utils import logout
from database import register_user, delete_user, update_profile
from constants import RECEPTIONIST, TUTOR


def manage_receptionists():
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
        register_user(name, password, email, RECEPTIONIST)
    elif choice == "2":
        email = input("Enter the employees email: ")
        delete_user(email)
    elif choice == "3":
        return
    else:
        raise Exception("Invalid choice. Try again")


def manage_tutor():
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
        classes = input("Enter employees classes separated by \',\': ").split(",")
        register_user(name, password, email, TUTOR, classes=classes)
    elif choice == "2":
        email = input("Enter the employees email: ")
        delete_user(email)
    elif choice == "3":
        return
    else:
        raise Exception("Invalid choice. Try again")


def view_monthly_income():
    pass


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
            manage_tutor()
        elif choice == "2":
            manage_receptionists()
        elif choice == "3":
            pass
        elif choice == "4":
            update_profile(user)
        elif choice == "5":
            return logout(user)
        else:
            raise Exception("Invalid choice. Try again")
