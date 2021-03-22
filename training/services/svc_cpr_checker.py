#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from datetime import datetime

def main():
    trainings = pd.read_csv("training_list_all_20210316.csv")
    trainings.fillna(int(0), inplace=True)


    staff = pd.read_csv("current_staff_list.csv")
    list = staff[staff["Employee Status"] == "Terminated"].index
    staff.drop(list, inplace=True)
    staff.fillna(0, inplace=True)
    
    
    # trainings = trainings['Course Name'].str.contains('CPR', na='Not Given')
    cpr = trainings[trainings["Course Name"].str.contains("CPR", na=False)]
    
    
    cpr.loc[:, "Date Taken"] = pd.to_datetime(cpr["Date Taken"], format="%m/%d/%Y")
    cpr.loc[:, "Date Last Modified"] = pd.to_datetime(
        cpr["Date Last Modified"], format="%m/%d/%Y"
    )
    cpr = cpr.rename(columns={"Employee ID": "PHS ID", "File No.": "Employee Id"})
    cpr = cpr.sort_values(by=["Date Taken", "Date Last Modified"], ascending=False)
    

    unfinished_list = cpr[
        (cpr["Remark"] == "Scheduled")
        | (cpr["Remark"] == "Cancelled")
        | (cpr["Remark"] == "No Show")
    ].index
    cpr.drop(unfinished_list, inplace=True)
    
    
    cpr = cpr.drop_duplicates(subset=["PHS ID"])
    
    
    for r in cpr.iterrows():
        index = r[0]
        if "Provisional" in r[1]["Course Name"]:
            cpr.loc[index, "Due Date"] = r[1]["Date Taken"] + pd.DateOffset(months=12)
        else:
            cpr.loc[index, "Due Date"] = r[1]["Date Taken"] + pd.DateOffset(months=24)


        cpr = cpr.sort_values(by=["Last Name"])
        cpr.reset_index(drop=True)


        cpr["Employee Id"] = cpr["Employee Id"].astype(int)
        merged = pd.merge(staff, cpr, on="Employee Id", how="outer")

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


        export.to_csv("cpr_export.csv", index=False)

if __name__ == "__main__":
    main()
