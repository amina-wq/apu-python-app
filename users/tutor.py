import database
from database import parse_txt
from database import update_profile
from utils import logout


def yes_or_no(saying="Do you want to finish? y/n\n"):
    while True:
        choice = input(saying)
        if choice == "y" or choice == "n":
            break
        else:
            print("please answer in y/n format")
    return choice == "y"


def show_available_classes(user, class_info):
    index = 1
    available_class_position = 0
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
    for available_class in available_classes:
        available_class_position = available_class.get("position")
        available_class.pop("index")
        available_class.pop("position")
        class_info[available_class_position] = available_class
    save(class_info)
    return class_info


def save(class_list) -> None:
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
                if key == list(line.keys())[-1]:
                    class_data += f"{key}:{value}"
                else:
                    class_data += f"{key}:{value};"
            file.write(class_data + "\n")


def tutor_menu(user):
    while True:
        menu = [
            "1. Show your classes",
            "2. Add class info",
            "3. Update/delete class info",
            "4. View students enrolled on your classes",
            "5. Update profile",
            "6. Create a new class",
            "7. Delete a class",
            "8. Logout",
        ]
        print("\n".join(menu))
        class_info = parse_txt("database/classes.txt")
        users = parse_txt("database/users.txt")
        choice = int(input())

        if choice == 1:
            available_classes = show_available_classes(user, class_info)
            print("\n")
            if yes_or_no("Do you want to see details of your classes? y/n\n"):
                for available_class in available_classes:
                    available_class.pop("index")
                    available_class.pop("position")
                    print(available_class)
            print("\n")

        elif choice == 2:
            while True:
                available_classes = show_available_classes(user, class_info)
                choice = int(
                    input("What class would you like to add information to\n")
                )
                for class_iterator in available_classes:
                    if class_iterator.get("index") == choice:
                        while True:
                            key = input(
                                "What type of info do you want to add?\n"
                            )
                            if class_info[class_iterator.get("position")].get(
                                key
                            ):
                                print("This information already exists")
                                continue
                            value = str(
                                input("What information do you want to add?\n")
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
                        )
                    )
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
                                    print("This information doesn`t exists")
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
                                    print("This information doesn`t exists")
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
                        set(user_iterator["subjects"]) & set(user["classes"])
                    ):
                        print(
                            user_iterator["nickname"],
                            " ",
                            list(
                                set(user_iterator["subjects"])
                                & set(user["classes"])
                            ),
                        )

        elif choice == 5:
            update_profile(user, menu_extension=["level"])

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
            if class_info[-1]:
                new_class["id"] = int(class_info[-1]["id"]) + 1
            else:
                new_class["id"] = 1
            class_info.append(new_class)
            for user_iterator in users:
                if user_iterator["email"] == user["email"]:
                    user_iterator["classes"].append(str(new_class["name"]))
                    user = user_iterator
                    break
            database.users = users
            database.save_users()
            save(class_info)

        elif choice == 7:
            available_classes = show_available_classes(user, class_info)
            choice = int(input("What class would you like to delete\n"))
            for available_class in available_classes:
                if available_class.get("index") == choice:
                    if not yes_or_no(
                        "Are you sure you want to"
                        " proceed with the deletion?"
                        " y/n\n"
                    ):
                        break
                    for user_iterator in users:
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
            logout(user)
            return None

        else:
            raise Exception("Invalid choice. Try again")
