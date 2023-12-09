def receptionist_menu(user):
    menu = [
        "1. Register Students",
        "2. Update Subject Enrollment",
        "3. Accept Payment and Generate Receipt",
        "4. Delete Completed Students",
        "5. Update profile",
        "6. Logout",
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
        pass
    elif choice == "5":
        pass
    elif choice == "6":
        pass
    else:
        raise Exception("Invalid choice. Try again")
