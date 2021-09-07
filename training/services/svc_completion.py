import datetime
import glob
import sys
import pandas as pd

import training.services.svc_report_data as data
import training.services.svc_report_maker as report_maker
import config

main_dir = config.main_path()
# test_df = pd.read_csv(main_dir / "master.csv")

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
    last_checked = data.log_check().strftime("%Y-%m-%d %H:%M")
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
    # print(df[df.index.duplicated()])
    # for r in range(0,len(df)):
    for r in range(0,len(df)):
        total_hours = 0
        hours_since_last_checked = 0
        d_hours = [0,0,0,0,0]  # Hours finished by deadline, #1-5
        deadlines =[[
            "Chapter 1",
            "Chapter 2",
            "Chapter 3"],
            ["Chapter 4",
             "Chapter 13",
             "Chapter 14"],
            ["Chapter 5",
             "Chapter 6",
             "Chapter 7"],
            ["Chapter 8",
             "Chapter 11",],
            ["Chapter 9",
             "Chapter 10",
             "Chapter 12"]]



        for c in chapters:
            test = df.iloc[r][c]
            try:
                test = str(test)
                test = datetime.datetime.strptime(test, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
                is_date= True
                hours = award_hours(c)
                if test > last_checked:
                    hours_since_last_checked += hours
                    # print("newer than check", hours_since_last_checked)
                # print('pass', test, last_checked)
                # print(c,"Hours: ", hours)
                total_hours += hours
                # print(df.iloc[r]['Name'],total_hours)
                if c in deadlines[0]:
                    d_hours[0] += hours
                elif c in deadlines[1]:
                    d_hours[1] += hours
                elif c in deadlines[2]:
                    d_hours[2] += hours
                elif c in deadlines[3]:
                    d_hours[3] += hours
                elif c in deadlines[4]:
                    d_hours[4] += hours

                # print(d_hours)
            except:
                is_date = False
                print(sys.exc_info())
                print("fail",test, last_checked)


        df.at[r,"Total Hours Completed"] = total_hours
        df.at[r,"Hours Completed Since Last Check"] = hours_since_last_checked
        df.at[r,"Due Date #1"] = d_hours[0]
        df.at[r,"Due Date #2"] = d_hours[1]
        df.at[r,"Due Date #3"] = d_hours[2]
        df.at[r,"Due Date #4"] = d_hours[3]
        df.at[r,"Due Date #5"] = d_hours[4]

    # print(df.loc[1])
    # print(df.loc[22])
    # print(df.loc[90])
    return df



    # for n in df:
        # Check Chapters for completion, if is date, is completed.
        # Check hours for completion, add to set total, completed total
        # Check date against last checked to see if hours are new, if so, add to new hours total.



if __name__ == "__main__":
    check_completion(test_df)
