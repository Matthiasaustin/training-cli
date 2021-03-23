#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from datetime import datetime


date = datetime.now().date()


def get_due_date_list(report_type=None):
    r_type = report_type or "CPR"
    trainings = pd.read_csv("training_list_all_20210316.csv")
    trainings.fillna(int(0), inplace=True)

    staff = pd.read_csv("current_staff_list.csv")
    list = staff[staff["Employee Status"] == "Terminated"].index
    staff.drop(list, inplace=True)
    staff.fillna(0, inplace=True)

    # trainings = trainings['Course Name'].str.contains('CPR', na='Not Given')
    report = trainings[trainings["Course Name"].str.contains(r_type, na=False)]

    report.loc[:, "Date Taken"] = pd.to_datetime(report["Date Taken"], format="%m/%d/%Y")
    report.loc[:, "Date Last Modified"] = pd.to_datetime(
        report["Date Last Modified"], format="%m/%d/%Y"
    )
    report = report.rename(columns={"Employee ID": "PHS ID",
                              "File No.": "Employee Id"})
    report = report.sort_values(by=["Date Taken", "Date Last Modified"],
                          ascending=False)


    unfinished_list = report[
        (report["Remark"] == "Scheduled")
        | (report["Remark"] == "Cancelled")
        | (report["Remark"] == "No Show")].index
    report.drop(unfinished_list, inplace=True)

    report = report.drop_duplicates(subset=["PHS ID"])

    for r in report.iterrows():
        index = r[0]
        if r_type.casefold() == 'CPR'.casefold():
            if "Provisional" in r[1]["Course Name"]:
                report.loc[index, "Due Date"] = r[1]["Date Taken"] + pd.DateOffset(months=12)
            else:
                report.loc[index, "Due Date"] = r[1]["Date Taken"] + pd.DateOffset(months=24)
        if r_type.casefold() == 'BBP'.casefold() or r_type.casefold() == 'Mandated'.casefold():
            report.loc[index, "Due Date"] = r[1]["Date Taken"] + pd.DateOffset(months=12)

        report = report.sort_values(by=["Last Name"])
        report.reset_index(drop=True)


        report["Employee Id"] = report["Employee Id"].astype(int)
        merged = pd.merge(staff, report, on="Employee Id", how="outer")

        export = merged[
            [
                "Employee Id",
                "First Name_x",
                "Last Name_x",
                "First Name_y",
                "Last Name_y",
                "Date Hired",
                "Primary Supervisor Name",
                "Primary Email",
                "Date Taken",
                "Due Date",
                "Remark",
            ]
        ]


        export.to_csv(f"{r_type}_export_{date}.csv", index=False)

def get_ce():
    print("Under Construction, try again later.")
    pass

if __name__ == "__main__":
    due_date_list()
