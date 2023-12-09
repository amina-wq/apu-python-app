from typing import Optional, List
from hashlib import md5


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
            dictionary = {}
            for part in parts:
                key, value = part.strip().split(":")
                if len(value.split(',')) > 1:
                    dictionary[key.strip()] = value.strip().split(',')
                else:
                    dictionary[key.strip()] = value.strip()
            data.append(dictionary)
    return data


users = parse_txt("database/users.txt")


def save_users() -> None:
    """The function overwrites the contents of the file
    after changes are made to the user list
    """
    with open("database/users.txt", "w") as file:
        for user in users:
            user_data = ""
            for key, value in user.items():
                if key == list(user.keys())[-1]:
                    if isinstance(value, list):
                        user_data += f"{key}:{','.join(value)}"
                    else:
                        user_data += f"{key}:{value}"
                else:
                    user_data += f"{key}:{value};"
            file.write(user_data + "\n")


def register_user(
    nickname: str, password: str, email: str, role: str, **kwargs
) -> None:
    """Function for registering a user and putting his/her profile into a text file
    Accepts mandatory and custom parameters.
    Args:
        nickname (str): user`s nickname
        password (str): user`s password
        email (str): user`s e-mail
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
        >>>     role=STUDENT, # noqa
        >>> )
    """
    user = {
        "nickname": nickname,
        "password": md5(password.encode()).hexdigest(),
        "email": email,
        "role": role,
    }
    user.update(kwargs)
    users.append(user)
    save_users()


def delete_user(email: str) -> None:
    """Delete user by e-mail"""
    for user in users:
        if user["email"] == email:
            users.remove(user)
            break
    save_users()


def update_profile(user: dict, menu_extension: Optional[list] = None) -> None:
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
    if user in users:
        menu = {
            "password": "1. Change password",
            "email": "2. Change email",
        }

        if menu_extension:
            menu.update(
                {
                    extension: f"{index}. Change {extension}"
                    for index, extension in enumerate(menu_extension, start=3)
                }
            )

        print("\n".join(menu.values()))

        while True:
            menu_choice = input("Enter your choice: ")
            if menu_choice.isdigit() and 0 < int(menu_choice) <= len(menu):
                break
        key = list(menu.keys())[int(menu_choice) - 1]

        new_value = input(f"Set new {key}: ")

        if user[key] == "password":
            new_value = md5(new_value.encode()).hexdigest()
        elif len(new_value.split(",")) > 1:
            new_value = new_value.split(",")
        user[key] = new_value

        save_users()
    else:
        raise ValueError("Incorrect user")
