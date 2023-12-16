from utils import login, show_menu


if __name__ == "__main__":
    while True:
        if user := login():
            show_menu(user)
        else:
            break
