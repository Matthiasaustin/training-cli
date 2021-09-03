import datetime
import glob
import sys
import pandas as pd

import training.services.svc_report_data as data
import training.services.svc_report_maker as report_maker
import config

main_dir = config.main_path()
test_df = pd.read_csv(main_dir / "master.csv")

def award_hours (chapter_number):
    """Chapter name must conform to the standard format, at which point it is matched with the correct number of hours to determine the number of hours to award."""

    return {
        "Chapter 1": 2.5,
        "Chapter 2": 2,
        "Chapter 3": 2.5,
        "Chapter 4": 4,
        "Chapter 5": 4,
        "Chapter 6": 1.5,
        "Chapter 7": 2,
        "Chapter 8": 4,
        "Chapter 9": 4,
        "Chapter 10": 2.5,
        "Chapter 11": 2.5,
        "Chapter 12": 6,
        "Chapter 13": 1.5,
        "Chapter 14": 2,
    }.get(chapter_number)


def check_completion (prepped_df, last_checked):
    """takes a df of student progress and checks completion and total hours finished."""
    df = prepped_df
    last_checked = data.log_check()


    # for each row in file

    # for each chapter listed
    # capture completion date, hours it is worth

    # if completion date is after last check, put in awarded col
    # if completion date is since last check, add to total col

    # columns=[
    #         "Chapter 1",
    #         "Chapter 2",
    #         "Chapter 3",
    #         "Due Date #1",
    #         "Chapter 4",
    #         "Chapter 13",
    #         "Chapter 14",
    #         "Due Date #2",
    #         "Chapter 5",
    #         "Chapter 6",
    #         "Chapter 7",
    #         "Due Date #3",
    #         "Chapter 8",
    #         "Chapter 11",
    #         "Due Date #4",
    #         "Chapter 9",
    #         "Chapter 10",
    #         "Chapter 12",
    #         "Due Date #5",
    #         "Total Hours Completed",
    #         "Total Hours Outstanding",]


if __name__ == "__main__":
    check_completion(test_df)
