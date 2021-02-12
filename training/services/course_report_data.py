import pandas as pd
import os, glob, sys, re
import datetime
import webbrowser
import shutil

class CourseDate():

    self.data_dir = os.path.abspath("../data")
    self.export_dir = os.path.abspath("../export")
    self.download_dir = os.path.abspath("/home/matthias/Downloads")
    
    self.downloads = os.path.join(download_dir,'completion-*')  # TODO May be alt way to do this (See click video or docs, not sure.)
    self.today = datetime.datetime.date(datetime.datetime.now())


def import_data():
    get_csv()
    path_list = import_path()
    dataframes = import_csvs(path_list)

    return dataframes


def get_csv():
    PATH = "../course_id.csv"
    course_id_df = pd.read_csv(PATH)
    course_ids = course_id_df.loc[:,'id']

    for k,v in course_ids.items():
        course_id = str(v)
        csv_url = f"https://dstrainings.com/report/completion/index.php?course={course_id}&format=csv"
        # print(csv_url)
        # webbrowser.open(csv_url)

    files = glob.glob(self.downloads)

    # TODO implement movement to data folder
    # for file in files:
    #     shutil.move(file,data_dir)


def import_path():

    user_path = "../data/"

    PATH = os.path.expanduser(user_path)

    # what type of files are read in
    EXT = "*.csv"

    # creates a list of specific locations to read from the path and extension
    path_list = glob.glob(os.path.join(PATH, EXT))

    # Sorts the list for easier handling later
    path_list.sort()

    return path_list


def get_month(file_path):
    """Uses regex to get month of completion report files files"""
    file = file_path
    month = re.search(r"-(.*?)_c", file)
    month = month.group()
    month = month.replace("-", "")
    month = month.replace("_c", "")
    month.strip()

    return month


def get_chapter(file_path):
"""Reviews the path and pulls out the chapter numbers."""
    chapter_number = re.search("chapter_\d\d", file)
    chapter_number = chapter_number.group()

    return chapter_number

def import_csvs():
    path_list = import_path()
    imported_csv_list = []
    for file in path_list:
        chapter_number = get_chapter(file)
        month = get_month(file)

        # reads the csv file in as a dataframe, fills any missing values with incomplete
        new_csv = pd.read_csv(file, parse_dates=["Course complete"], dayfirst=True)
        new_csv.fillna("Incomplete", inplace=True)

        new_csv["Chapter"] = chapter_number
        new_csv["Month"] = month

        imported_csv_list.append(new_csv)

    return imported_csv_list
