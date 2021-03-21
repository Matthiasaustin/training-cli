#Config information for course info
from pathlib import Path


def main_path():
    main_p = Path(__file__).parent
    return main_p

def send_info():
    main = main_path()
    send_path = main / "email_data/send_info/"

    return send_path


if __name__ == "__main__":
    main_path()
    send_info()
