from database import update_profile
from utils import logout


def student_menu(user):
    menu = [
        "1. Class Schedule",
        "2. Change subject",
        "3. Course Fee",
        "4. Update profile",
        "5. Logout",
    ]
    print("\n".join(menu))
    choice = input("Enter your choice: ")
    if choice == "1":
        pass
    elif choice == "2":
        pass
    elif choice == "3":
        pass
    elif choice == "4":
        update_profile(user)
    elif choice == "5":
        return logout(user)
    else:
        raise Exception("Invalid choice. Try again")
