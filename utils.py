from constants import ADMIN, RECEPTIONIST, TUTOR, STUDENT
from database import users


def logout():
    raise NotImplementedError


def login():
    """User login function. Has a limit of 3 login attempts
    Returns:
        Optional(dict): selected user or None if user has not been selected
    """
    selected_user = None
    attempts = 3
    while attempts > 0:
        email = input("Enter email: ")
        password = input("Enter password: ")
        for user in users:
            if user["email"] == email and user["password"] == password:
                selected_user = user
                break
        else:
            attempts -= 1
            print("Invalid email or password")
            continue
        break

    if not selected_user:
        print("Too many attempts")
    return selected_user


def show_menu(user):
    """Displays menu depending on the users role"""
    from admin import admin_menu
    from receptionist import receptionist_menu
    from tutor import tutor_menu
    from student import student_menu

    role = user.get("role")

    if role == ADMIN:
        admin_menu(user)
    elif role == RECEPTIONIST:
        receptionist_menu(user)
    elif role == TUTOR:
        tutor_menu(user)
    elif role == STUDENT:
        student_menu(user)
    else:
        raise Exception("User unfounded")
