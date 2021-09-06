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


def check_completion (prepped_df):
    """takes a df of student progress and checks completion and total hours finished."""
    df = prepped_df
    last_checked = data.log_check().strftime("%Y-%m-%d")
    print("last check: ", last_checked)
    chapters = [
        "Chapter 1",
        "Chapter 2",
        "Chapter 3",
        "Chapter 4",
        "Chapter 5",
        "Chapter 6",
        "Chapter 7",
        "Chapter 8",
        "Chapter 9",
        "Chapter 10",
        "Chapter 11",
        "Chapter 12",
        "Chapter 13",
        "Chapter 14",
    ]
    print(len(df))
    # tests = [df.iloc[1]['Chapter 1'],
    #          df.iloc[2]['Chapter 1'],
    #          df.iloc[44]['Chapter 1'],
    #          df.iloc[45]['Chapter 1'],
    #          "Started(44%)",
    #          ]
    # for r in range(0,len(df)):


    for r in range(0,15):
        for c in chapters:
            try:
                test = datetime.datetime.strptime(df.iloc[r][c], "%Y-%m-%d").strftime("%Y-%m-%d")
                is_date= True
                print(test, last_checked)
                if test > last_checked:
                    print("newer than check")
                if test < last_checked:
                    print("older than last check")
                print('pass', test)
            except:
                is_date = False
                print("fail", test)
            print(is_date)







    # for n in df:
        # Check Chapters for completion, if is date, is completed.
        # Check hours for completion, add to set total, completed total
        # Check date against last checked to see if hours are new, if so, add to new hours total.



if __name__ == "__main__":
    check_completion(test_df)
