#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from datetime import datetime
from pathlib import Path

date = datetime.now().date()


def get_due_date_list(report_type=None):
    r_type = report_type or "CPR"

    # Set target directory, currrently Downloaded
    downloads_dir = Path.home() / "Downloads"

    # Prompt use to move file into correct directory and input filename
    training_list = downloads_dir / Path(
        input(
            "Place your training list csv file in the \'Downloads\' folder and then type in its name here (i.e. file_name.csv)\File name: "
        ))

    # Read csv indicated and fill empty values with 0 for later processing
    trainings = pd.read_csv(training_list)
    trainings.fillna(int(0), inplace=True)

    # Prompt use to move file into correct directory and input filename
    staff_list = downloads_dir / Path(
        input(
            "Place your staff list in the \'Downloads\' folder and type its full name.\n File Name: "
        ))

    # Read csv indicated and fill empty values with 0 for later processing, also drop non-active employees.
    staff = pd.read_csv(staff_list)
    list = staff[staff["Employee_Status"] == "Terminated"].index
    staff.drop(list, inplace=True)
    staff.fillna(0, inplace=True)

    # trainings = trainings['Course Name'].str.contains('CPR', na='Not Given')
    report = trainings[trainings["Course Name"].str.contains(r_type, na=False)]

    report.loc[:, "Date Taken"] = pd.to_datetime(report["Date Taken"],
                                                 format="%m/%d/%Y")
    report.loc[:, "Date Last Modified"] = pd.to_datetime(
        report["Date Last Modified"], format="%m/%d/%Y")
    report = report.rename(columns={
        "Employee ID": "PHS ID",
        "File No.": "Employee Id"
    })
    report = report.sort_values(by=["Date Taken", "Date Last Modified"],
                                ascending=False)

    unfinished_list = report[(report["Remark"] == "Scheduled")
                             | (report["Remark"] == "Cancelled")
                             | (report["Remark"] == "No Show")].index
    report.drop(unfinished_list, inplace=True)

    report = report.drop_duplicates(subset=["PHS ID"])

    for r in report.iterrows():
        index = r[0]
        if r_type.casefold() == 'CPR'.casefold():
            if "Provisional".casefold() in r[1]["Course Name"].casefold():
                report.loc[index,
                           "Due Date"] = r[1]["Date Taken"] + pd.DateOffset(
                               months=12)
            elif "Extension".casefold() in r[1]["Course Name"].casefold():
                report.loc[index,
                           "Due Date"] = r[1]["Date Taken"] + pd.DateOffset(
                               months=4)
            else:
                report.loc[index,
                           "Due Date"] = r[1]["Date Taken"] + pd.DateOffset(
                               months=24)
        if r_type.casefold() == 'BBP'.casefold() or r_type.casefold(
        ) == 'Mandated'.casefold():
            report.loc[index, "Due Date"] = r[1]["Date Taken"] + pd.DateOffset(
                months=12)

        report = report.sort_values(by=["Last Name"])
        report.reset_index(drop=True)

        report["Employee Id"] = report["Employee Id"].astype(int)
        merged = pd.merge(staff, report, on="Employee Id", how="outer")

        export = merged[[
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
        ]]

        export.to_csv(f"{r_type}_export_{date}.csv", index=False)


def get_ce():
    print("Under Construction, try again later.")
    pass


if __name__ == "__main__":
    due_date_list()
