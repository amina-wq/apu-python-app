import os
from shutil import copyfile
from typing import Optional, List, Dict, Any
from hashlib import md5

from constants import ROLES_PRIORITY_MAPPER


def parse_txt(path: str) -> List[dict]:
    """The function parses a txt file of the form
        key1:value1;key2:value2...
        key1:value3;key2:value4...
    In the list of dictionaries of the form:
        [
            {
                key1: value1,
                key2: value2,
            },
            {
                key1: value3,
                key2: value4,
            },
        ]

    Args:
        path (str): path to txt file to parse from
    Returns:
        list: list of dictionaries parsed from txt file
    """
    with open(path) as file:
        data = []
        for line in file:
            parts = line.split(";")
            dictionary: Dict[str, Any | List[Any]] = {}
            for part in parts:
                key, value = part.strip().split(":")
                if len(value.split(",")) > 1:
                    dictionary[key.strip()] = value.strip().split(",")
                elif value.strip() in ["True", "False"]:
                    dictionary[key.strip()] = value.strip() == "True"
                else:
                    dictionary[key.strip()] = value.strip()
            data.append(dictionary)
    return data


users = parse_txt("database/users.txt")
classes = parse_txt("database/classes.txt")
requests = parse_txt("database/requests.txt")


def save(path: str, data: List[dict], need_backup: bool = False) -> list:
    """Saves data from list to file in key1:value1;key2:value2;... format
    You can make backup of file before saving to prevent issues with database

    Args:
        path(str): path to the file to which the data will be saved
        data(list(dict)): data to be saved
        need_backup(bool): True if backup of the file needed, False otherwise

    Returns:
        (list(dict)): saved data
    """
    if need_backup:
        filename, extension = os.path.splitext(os.path.basename(path))
        directory = os.path.dirname(path)
        backup_path = os.path.join(directory, f"{filename}_backup{extension}")
        copyfile(path, backup_path)

    try:
        with open(path, "w") as file:
            for dictionary in data:
                row_data = ""
                for key, value in dictionary.items():
                    postfix = "" if key == list(dictionary.keys())[-1] else ";"
                    if isinstance(value, list):
                        row_data += f"{key}:{','.join(value)}" + postfix
                    else:
                        row_data += f"{key}:{value}" + postfix
                file.write(row_data + "\n")
        return data
    except Exception:
        if need_backup:
            copyfile(backup_path, path)
            print("An error occurred. The database backup was restored.")
            return parse_txt(path)
        else:
            print("An error while saving occurred.")
            return data


def register_user(nickname: str, password: str, email: str, contact_number: str, role: str, **kwargs) -> None:
    """Function for registering a user and putting his/her profile into a text file
    Accepts mandatory and custom parameters.
    Args:
        nickname (str): user`s nickname
        password (str): user`s password
        email (str): user`s e-mail
        contact_number (int): user's phone number
        role (str): any role from the list of the constants: [ADMIN, RECEPTIONIST, TUTOR, STUDENT]
        kwargs: Any other key:value parameter to put into user profile
    Examples:
        >>> register_user("superman", "superman123", "superman123@gmail.com", ADMIN) # noqa
        or
        >>> register_user("genius12", "qwerty", "genius12@gmail.com", TUTOR, subjects=[MATH, ENGLISH]) # noqa
        or
        >>> register_user(
        >>>     nickname="good_person",
        >>>     password="person51",
        >>>     email="good@gmail.com",
        >>>     contact_number="017233899",
        >>>     role=STUDENT, # noqa
        >>> )
    """
    user = {
        "nickname": nickname,
        "password": md5(password.encode()).hexdigest(),
        "email": email,
        "contact_number": contact_number,
        "role": role,
    }

    user.update(kwargs)

    if any(";" in arg or ":" in arg for arg in user.values() if isinstance(arg, str)):
        print('You can\'t use ";" and ":", try again')
        return

    print("User was registered successfully")

    global users
    users.append(user)
    users = save("./database/users.txt", users, need_backup=True)


def delete_user(own_user: dict, email: str) -> None:
    """Delete user by e-mail"""
    global users
    for user in users:
        if user["email"] == email:
            if ROLES_PRIORITY_MAPPER[user["role"]] > ROLES_PRIORITY_MAPPER[own_user["role"]]:  # type: ignore
                raise ValueError("You can not delete this user")
            users.remove(user)
            print("User was deleted successfully")
            break
    else:
        print("The user with this email doesn't exist")
    users = save("./database/users.txt", users, need_backup=True)


def update_profile(user: Dict[str, Any | List[Any]], menu_extension: Optional[list] = None) -> None:
    """
    Updates users profile in text file
    Args:
        user (dict): user that should be updated
        menu_extension (list): optional list of updatable parameters of user
    Examples:
        >>> update_profile(user)
        1. Change password
        2. Change email
        Enter your choice: 1
        Set new password: qwerty

        or

        >>> update_profile(user, menu_extension=['subjects', 'age'])
        1. Change password
        2. Change email
        3. Change subjects
        4. Change age
        Enter your choice: 4
        Set new age: 15
    """
    global users

    if user in users:
        menu = {
            "nickname": "1. Change name",
            "password": "2. Change password",
            "contact_number": "3. Change contact number",
        }

        if menu_extension:
            menu.update(
                {extension: f"{index}. Change {extension}" for index, extension in enumerate(menu_extension, start=4)}
            )
        while True:
            print("\n".join(menu.values()))
            menu_choice = input("Enter your choice: ")
            if menu_choice.isdigit() and 0 < int(menu_choice) <= len(menu):
                break
            else:
                print("Invalid input, try again")
        key = list(menu.keys())[int(menu_choice) - 1]

        new_value = input(f"Set new {key}: ")
        if ";" in new_value or ":" in new_value:
            print(f'You can\'t use ";" and ":" in {key}, try again')
            return

        if key == "password":
            hashed_password = md5(new_value.encode()).hexdigest()
            user[key] = hashed_password
        elif isinstance(user[key], bool):
            user[key] = new_value == "True"
        elif len(new_value.split(",")) > 1:
            values_list = new_value.split(",")
            user[key] = values_list
        else:
            user[key] = new_value

        users = save("./database/users.txt", users, need_backup=True)
        print(f"The {key} was updated successfully")
    else:
        print("Incorrect user")


def get_user_by_email(own_user: dict, email: str, role: Optional[str] = None):
    user = next(iter([user for user in users if user["email"] == email]), None)
    if user:
        if role and user["role"] != role:
            return None
        if ROLES_PRIORITY_MAPPER[user["role"]] > ROLES_PRIORITY_MAPPER[own_user["role"]]:  # type: ignore
            raise ValueError("You don't have access to get this user")
    return user


def get_users_by_role(role: str):
    return [user for user in users if user["role"] == role]
