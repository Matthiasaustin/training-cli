from credential_finder.config import (
    WA_DATA_USER_NAME,
    WA_DATA_PASSWORD,
    WA_DATA_API_KEY,
)
import pandas as pd
from sodapy import Socrata
from datetime import datetime
import os
import glob


class Person:
    def __init__(
        self,
        first_name=None,
        last_name=None,
        birthday=None,
        birthyear=None,
        credential_number=None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.birthyear = datetime.strptime(birthday, "%m/%d/%Y").year
        self.credential_number = (
            credential_number  # Credential number on staff certificate.
        )


class Check:
    def __init__(self, api_key=None, username=None, password=None):
        api_key = api_key or WA_DATA_API_KEY
        username = username or WA_DATA_USER_NAME
        password = password or WA_DATA_PASSWORD
        self.records_code = "qxh8-f4bd"
        self.client = Socrata("data.wa.gov", api_key, username, password)
        self.check_list = None  # Path to csv file with list of staff to check.

    def check_single_record(
        self, first_name=None, last_name=None, birthday=None, credential_number=None
    ):
        first_name = first_name
        last_name = last_name
        birthyear = datetime.strptime(birthday, "%m/%d/%Y").year

        # expiration_date = datetime.strftime(birthday)
        credential_number = credential_number
        if credential_number is not None:
            results = self.client.get(
                self.records_code, credentailnumber=credential_number
            )
            print(results)
        else:
            results = self.client.get(
                self.records_code,
                firstname=first_name,
                lastname=last_name,
                birthyear=birthyear,
            )

            print(results)
        results = pd.DataFrame.from_records(results)
        output = []

        for result in results.iterrows():
            r = f"""
            First Name: {result[1]['firstname']}
            Last Name: {result[1]['lastname']}
            Credential Number: {result[1]['credentialnumber']}
            Status: {result[1]['status']}
            Next Expiration: {result[1]['expirationdate']}
            """
            output.append(r)
        return output

    # def check_current(expiration_date):
    #    expiration_date = datetime.strptime(expiration_date, "%Y%m%d")
    def check_file(file_path=None, file_type=None):
        if file_type is None:
            types = {"CSV": "csv", "Excel": "xlsx", "JSON": "json"}
            x = 0
            for k, v in types.items():
                print(f"{x+1}: {k}")
                x += 1
            c = int(input("Which number is your choice?\n")) - 1

            file_type = list(types.values())[c]
            print(file_type)

        else:
            file_type = file_type

        if file_path is None:
            PATH = file_path
        else:
            files = os.path.join(os.path.expanduser("~/Downloads"), f"*.{file_type}")
            files = glob.glob(files)
            choices = {}
            print("Would you like to use:\n")
            key = 0
            for i in files:
                i = i.replace((os.path.expanduser("~/Downloads/")), "").replace(
                    f".{file_type}", ""
                )
                print(f"{key+1}: {i}")
                choices[key] = i
                key += 1
            while True:
                try:
                    while True:
                        try:
                            choice = int(input("Choice:  ").strip())
                        except ValueError:
                            x = input(
                                "Your input isn't a choice listed.\nWant to quit? y to quit, any other key to continue:\n"
                            )
                            if x.lower() == "y":
                                return exit()
                            else:
                                continue
                        break
                    PATH = os.path.join(
                        os.path.expanduser("~/Downloads/"),
                        str(choices[choice - 1]) + f".{file_type}",
                    )
                except KeyError:
                    print("Looks like your choice didn't work, try again!")
                    continue
                else:
                    return


if __name__ == "__main__":
    print("Running the Service: Checker")

    Check().check_file()
