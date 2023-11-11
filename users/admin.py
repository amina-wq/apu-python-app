from utils import logout
from database import register_user, delete_user, update_profile
from constants import RECEPTIONIST


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
            pass
        elif choice == "2":
            manage_receptionists()
        elif choice == "3":
            pass
        elif choice == "4":
            update_profile(user)
        elif choice == "5":
            logout()
        else:
            raise Exception("Invalid choice. Try again")
