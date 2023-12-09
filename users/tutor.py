from database import parse_txt
from database import update_profile
from utils import logout


def tutor_menu(user):
    print(
        "1. Show your classes\n"
          "2. Add class info\n"
          "3. Update/delete class info\n"
          "4. View students enrolled\n"
          "5. Update profile\n"
          "6. Logout"
          )
    class_info = parse_txt("database/classes.txt")

    users = parse_txt("database/users.txt")
    command = int(input())
    if command == 1:
        show_available_classes(user, class_info)
    elif command == 2:
        available_classes = show_available_classes(user, class_info)
        command = int(input("What class would you like to add information to "))
        for i in available_classes:
            if i.get("index") == command:
                while True:
                    key = input("What type of info do you want to add? ")
                    if class_info[i.get('position')].get(key):
                        print("This information already exists")
                        continue
                    value = input("What information do you want to add?")
                    i[key] = value
                    break
        merge_classes(available_classes, class_info)

    elif command == 3:
        command = int(
            input("Do you want to update(1) or delete(2) class information?"
                  " To cancel this action type any other symbol")
        )

        if command == 1:
            available_classes = show_available_classes(user, class_info)
            command = int(
                input("What class would you like to change information of "))
            for i in available_classes:
                if i.get("index") == command:
                    while True:
                        key = input("What type of info do you want to add? ")
                        if class_info[i.get("position")].get(key) is None:
                            print("This information doesn`t exists")
                            continue
                        value = input("What information do you want to add?")
                        i[key] = value
                        break
            merge_classes(available_classes, class_info)

        elif command == 2:
            print("What information do you want to delete?")
            available_classes = show_available_classes(user, class_info)
            command = int(input("What class would you like to delete information of "))
            for i in available_classes:
                if i.get('index') == command:
                    while True:
                        key = input("What type of info do you want to delete? ")
                        if class_info[i.get("position")].get(key) is None:
                            print("This information doesn`t exists")
                            continue
                        if (
                                key == "name"
                                or key == "start"
                                or key == "end"
                                or key == "id"
                        ):
                            i[key] = None
                        else:
                            i.pop(key)
                        break
            merge_classes(available_classes, class_info)


    elif command == 4:
        for i in users:
            if i["role"] == "Student":
                if common_check(i, user, class_info):
                    print(i["nickname"], " ", common_check(i, user, class_info))




    elif command == 5:
        update_profile(user)

    elif command == 6:
        logout()

    else:
        print("incorrect input")
    tutor_menu(user)


def show_available_classes(user, class_info):
    index = 1
    available_class_position = 0
    available_classes = []
    for i in class_info:
        if i["id"] in lister(user["class_id"]):
            print(
                f"{index}. {i.get('name')} ({i.get('start')}-{i.get('end')})"
            )
            available_classes.append(
                {"position": available_class_position, "index": index}
            )
            index += 1
        available_class_position += 1
    return available_classes


def merge_classes(available_classes, class_info):
    for i in available_classes:
        available_class_position = i.get("position")
        i.pop("index")
        i.pop("position")
        class_info[available_class_position].update(i)
    save(class_info)
    return class_info


def save(class_list) -> None:
    with open("database/classes.txt", "w") as file:
        for i in class_list:
            class_data = ""
            for key, value in i.items():
                if key == list(i.keys())[-1]:
                    class_data += f"{key}:{value}"
                else:
                    class_data += f"{key}:{value};"
            file.write(class_data + "\n")


def lister(string):
    return string.split(",")


def common_check(student, user, classes):
    common_classes = []
    for i in lister(student["class_id"]):
        for j in lister(user["class_id"]):
            if i == j:
                for h in classes:
                    if h["id"] == i:
                        common_classes.append(h["name"])
    return common_classes
