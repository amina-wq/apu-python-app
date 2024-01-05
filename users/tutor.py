import database
from database import parse_txt
from database import update_profile
from utils import logout


def yes_or_no(saying="Do you want to finish? y/n\n"):
    """The function asks user a question, that when is being responded
        with y/n returns TRUE or FALSE respectively
    Args:
        saying(str): question that user is supposed to answer
    Returns:
        choice: TRUE or FALSE, depending on if the answer is y or n
    """
    while True:
        choice = input(saying)
        if choice == "y" or choice == "n":
            break
        else:
            print("please answer in y/n format")
    return choice == "y"


def show_available_classes(user, class_info):
    """The function prints classes that are available to a user
        Example of printed classes:
         1. name_of_the_class1
         2. name_of_the_class2
         3. name_of_the_class3
       and returns them in a list.
        Example of the function returned output
         [
         {
            position:value1,
            index:value2,
            key3:value3,
            key4:value4
         }
         ]
    Args:
        user: user whose class availability is checked
        class_info: list of all classes
    Returns:
        available_classes: list of available to the user classes
    """
    index = (
        1  # index is a convenient number by which user can address the class
    )
    available_class_position = (
        0  # position indicates position of a class in a class_info list
    )
    available_classes = []
    for class_interator in class_info:
        if class_interator["name"] in user["classes"]:
            print(
                f"{index}. {class_interator.get('name')}"
                f" ({class_interator.get('start')}"
                f"-{class_interator.get('end')})"
            )
            available_classes.append(
                {"position": available_class_position, "index": index}
            )
            available_classes[index - 1].update(class_interator)
            index += 1
        available_class_position += 1
    return available_classes


def merge_classes(available_classes, class_info):
    """The function merges a modified fragment of the list of classes
       to the list of classes itself, updating class details
    Args:
        available_classes: modified list of classes available to user
        class_info: list of all classes
    Returns:
        class_info: updated list of all classes
    """
    for available_class in available_classes:
        available_class_position = available_class.get(
            "position"
        )  # variable that remembers position of a class
        available_class.pop("index")
        available_class.pop("position")
        class_info[available_class_position] = available_class
    save(class_info)
    return class_info


def save(class_list) -> None:
    """The function saves the list of classes to the text file in the
    database, by overwriting the information in the text file
    """
    with open("database/classes.txt", "w") as file:
        for line in class_list:
            class_data = ""
            for key, value in line.items():
                if type(value) is list:
                    value = (
                        str(value)
                        .replace(" ", "")
                        .strip("[")
                        .strip("]")
                        .replace("'", "")
                    )
                if (
                    key == list(line.keys())[-1]
                ):  # check if the key is last in the dictionary
                    class_data += (
                        f"{key}:{value}"  # if so, ";" must not be placed
                    )
                else:
                    class_data += (
                        f"{key}:{value};"  # otherwise, ";" must be placed
                    )
            file.write(class_data + "\n")


def tutor_menu(user):
    """The main function of the tutor functionality. It displays to
    users Tutor menu and gives them access to Tutor functionality.
    Args:
        user: The user for whom the tutor menu is displayed.

    Returns:
        None
    """
    menu = [
        "1. Show your classes",
        "2. Add class info",
        "3. Update/delete class info",
        "4. View students enrolled in your classes",
        "5. Update profile",
        "6. Create a new class",
        "7. Delete a class",
        "8. Logout",
    ]

    while True:
        print("\n".join(menu))
        class_info = parse_txt("database/classes.txt")
        users = parse_txt(
            "database/users.txt"
        )  # this parse_txt function imported from database.py
        print("\nEnter your choice\n")
        choice = int(input())

        try:
            if choice == 1:
                available_classes = show_available_classes(user, class_info)
                print("\n")
                if yes_or_no(
                    "Do you want to see details of your classes? y/n\n"
                ):
                    for available_class in available_classes:
                        available_class.pop("index")
                        available_class.pop("position")
                        print(available_class)
                print("\n")

            elif choice == 2:
                while True:
                    available_classes = show_available_classes(
                        user, class_info
                    )
                    choice = int(
                        input(
                            "What class would you like to add information to\n"
                            " (write 0 if you want to quit)\n"
                        )
                    )
                    if choice > available_classes[-1]["index"]:
                        raise Exception("Invalid choice. Try again")
                    for class_iterator in available_classes:
                        if class_iterator.get("index") == choice:
                            while True:
                                key = input(
                                    "What type of information"
                                    " do you want to add?\n"
                                )
                                if class_info[
                                    class_iterator.get("position")
                                ].get(key):
                                    print("This information already exists")
                                    continue
                                value = str(
                                    input(
                                        "What information"
                                        " do you want to add?\n"
                                    )
                                ).replace(" ", "")
                                class_iterator[key] = value
                                break
                    merge_classes(available_classes, class_info)
                    if yes_or_no():
                        break

            elif choice == 3:
                choice = int(
                    input(
                        "Do you want to update(1)"
                        " or delete(2) class information?\n"
                        " To cancel this action type any other symbol\n"
                    )
                )

                if choice == 1:
                    while True:
                        available_classes = show_available_classes(
                            user, class_info
                        )
                        choice = int(
                            input(
                                "What class would you like"
                                " to change information of\n"
                                " (write 0 if you want to quit)\n"
                            )
                        )
                        if choice > available_classes[-1]["index"]:
                            raise Exception("Invalid choice. Try again")
                        for available_class in available_classes:
                            if available_class.get("index") == choice:
                                print(
                                    "Information of this class"
                                    " before the changes:\n",
                                    class_info[available_class["position"]],
                                )
                                while True:
                                    key = input(
                                        "What type of info do you want"
                                        " to change?\n"
                                    )
                                    if (
                                        class_info[
                                            available_class.get("position")
                                        ].get(key)
                                        is None
                                    ):
                                        print(
                                            "This information doesn`t exists"
                                        )
                                        continue
                                    value = str(
                                        input(
                                            "What information do you want to"
                                            " take its place?\n"
                                        )
                                    ).replace(" ", "")
                                    available_class[key] = value
                                    break
                        merge_classes(available_classes, class_info)
                        if yes_or_no():
                            break

                elif choice == 2:
                    while True:
                        print("What information do you want to delete?")
                        available_classes = show_available_classes(
                            user, class_info
                        )
                        choice = int(
                            input(
                                "What class would you like"
                                " to delete information of\n"
                                " (write 0 if you want to quit)\n"
                            )
                        )
                        if choice > available_classes[-1]["index"]:
                            raise Exception("Invalid choice. Try again")
                        for available_class in available_classes:
                            if available_class.get("index") == choice:
                                print(
                                    "Information of this class"
                                    " before the changes:\n",
                                    class_info[available_class["position"]],
                                )
                                while True:
                                    key = input(
                                        "What type of info do you want"
                                        " to delete?\n"
                                    )
                                    if not yes_or_no(
                                        "Are you sure you want to"
                                        " proceed with the deletion?"
                                        " y/n\n"
                                    ):
                                        break
                                    if (
                                        class_info[
                                            available_class.get("position")
                                        ].get(key)
                                        is None
                                    ):
                                        print(
                                            "This information doesn`t exists"
                                        )
                                        break
                                    if key in [
                                        "name",
                                        "start",
                                        "end",
                                        "dates",
                                        "charge",
                                        "level",
                                    ]:
                                        available_class[key] = None
                                    else:
                                        del available_class[key]
                                    break
                        merge_classes(available_classes, class_info)
                        if yes_or_no():
                            break

            elif choice == 4:
                for user_iterator in users:
                    if user_iterator["role"] == "Student":
                        if list(
                            set(user_iterator["subjects"])
                            & set(user["classes"])
                        ):  # Check if the list of student subjects
                            # and list of tutor classes intersect
                            print(
                                user_iterator["nickname"],
                                " ",
                                list(
                                    set(user_iterator["subjects"])
                                    & set(user["classes"])
                                ),
                                # Printing an intersections into the console
                            )

            elif choice == 5:
                update_profile(
                    user
                )  # Function update_profile is imported from database.py

            elif choice == 6:
                new_class = {}
                print("What`s the name of this class?")
                new_class["name"] = str(input()).replace(" ", "")
                print("What`s the monthly for this class")
                new_class["charge"] = str(input()).replace(" ", "")
                print("What`re the week days of this class(E.g. mon,tue,fri)")
                new_class["dates"] = str(input()).replace(" ", "").split(",")
                print("At what time does this class start?(E.g. 14.00)")
                new_class["start"] = str(input()).replace(" ", "")
                print("At what time does this class end?(E.g. 16.00)")
                new_class["end"] = str(input()).replace(" ", "")
                if class_info[
                    -1
                ]:  # Check if it`s the first class to be created in the file
                    new_class["id"] = int(class_info[-1]["id"]) + 1
                else:
                    new_class["id"] = 1
                class_info.append(new_class)
                for (
                    user_iterator
                ) in users:  # Function that adds the name of a class
                    # to tutor that created it
                    if user_iterator["email"] == user["email"]:
                        user_iterator["classes"].append(str(new_class["name"]))
                        user = user_iterator
                        break
                database.users = users
                database.save_users()
                save(class_info)

            elif choice == 7:
                available_classes = show_available_classes(user, class_info)
                choice = int(
                    input(
                        "What class would you like to delete?\n"
                        " (write 0 if you want to quit)\n"
                    )
                )
                if choice > available_classes[-1]["index"]:
                    raise Exception("Invalid choice. Try again")
                for available_class in available_classes:
                    if available_class.get("index") == choice:
                        if not yes_or_no(
                            "Are you sure you want to"
                            " proceed with the deletion?"
                            " y/n\n"
                        ):
                            break
                        for (
                            user_iterator
                        ) in (
                            users
                        ):  # Function that removes the name of a class
                            # from tutor that teaches it
                            if user_iterator["email"] == user["email"]:
                                user_iterator["classes"].remove(
                                    available_class["name"]
                                )
                                user = user_iterator
                                break
                        del class_info[available_class["position"]]
                        database.users = users
                        database.save_users()
                        save(class_info)
                        break

            elif choice == 8:
                logout(user)  # This function is imported from utils.py
                return None

            else:
                raise ValueError("Invalid choice. Try again")

        except Exception:
            print("Something went wrong, please try again")
            continue
