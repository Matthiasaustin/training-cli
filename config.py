# Config information for course info
from getpass import getpass
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

# WA Data Credentials
# WA_DATA_USER_NAME = input(
#     "What username would you like to use for WA Data?\nUsername: "
# )
# WA_DATA_PASSWORD = getpass(
#     "What password would you like to use for WA Data?\nPassword: "
# )
# WA_DATA_API_KEY = getpass("What api key would you like to use for WA Data?\nAPI Key: ")
