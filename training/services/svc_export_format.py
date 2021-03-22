import pandas as pd
from datetime import datetime
import os
import glob
import sys
import re

today = datetime.date(datetime.now())


class formats:
    def __init__(self, workbook, worksheet):
        self.workbook = workbook
        self.worksheet = worksheet

        self.complete_format = workbook.add_format({"bg_color": "#90F685"})

        self.stale_format = workbook.add_format({"bg_color": "#82E0AA", "bold": 1})
        self.closed_format = workbook.add_format(
            {"bg_color": "#F2F4F4", "font_color": "#F2F4F4", "pattern": 1}
        )
        self.not_enrolled = workbook.add_format(
            {"bg_color": "#F2F4F4", "font_color": "#F2F4F2", "pattern": 1}
        )
        self.highlight_format = workbook.add_format(
            {
                "bold": 1,
                "bg_color": "#58D68D",
                "border": 6,
                "border_color": "red",
                "align": "center",
                "valign": "center",
            }
        )

        self.started_format = workbook.add_format({"bg_color": "#F9E79F"})
        self.incomplete_format = workbook.add_format({"bg_color": "#EDBB99"})
        self.not_enrolled = workbook.add_format(
            {"bg_color": "#F2F4F4", "font_color": "#F2F4F2", "pattern": 1}
        )
        self.location = "A5:BF100"

    def con_closed1(self):
        return {
            "type": "formula",
            "criteria": '=ISNUMBER(SEARCH("Closed",$O$2)) ',
            "value": "Closed",
            "format": self.closed_format,
        }

    def con_closed2(self):
        return {
            "type": "formula",
            "criteria": '=ISNUMBER(SEARCH("Closed",$V$2)) ',
            "value": "Closed",
            "format": self.closed_format,
        }

    def con_notenrolled(self):
        return {
            "type": "text",
            "criteria": "containing",
            "value": "Not Enrolled",
            "format": self.not_enrolled,
        }
        self.complete_format = workbook.add_format({"bg_color": "#90F685"})

        self.stale_format = workbook.add_format({"bg_color": "#82E0AA", "bold": 1})
        self.highlight_format = workbook.add_format(
            {
                "bold": 1,
                "bg_color": "#58D68D",
                "border": 6,
                "border_color": "red",
                "align": "center",
                "valign": "center",
            }
        )

        self.started_format = workbook.add_format({"bg_color": "#F9E79F"})
        self.incomplete_format = workbook.add_format({"bg_color": "#EDBB99"})
        self.location = "A5:BF100"

    def con_complete(self):
        return {
            "type": "text",
            "criteria": "containing",
            "value": "Finished",
            "format": self.complete_format,
        }

    def con_notstarted(self):
        return {
            "type": "text",
            "criteria": "containing",
            "value": "Not Started",
            "format": self.incomplete_format,
        }

    def con_blanks(self):
        blanks = {"type": "blanks", "format": self.incomplete_format}
        return blanks

    def con_started(self):
        return {
            "type": "text",
            "criteria": "containing",
            "value": "Started",
            "format": self.started_format,
        }

    def date_format(self):
        return {
            "type": "time_period",
            "num_format": "%mm/%dd/%yy"
        }

    def date(self):
        return {
            "type": "time_period",
            "criteria": "last 7 days",
            "format": self.highlight_format,
        }

    def stale_date(self):
        return {
            "type": "date",
            "criteria": "less than",
            "value": datetime.now(),
            "format": self.stale_format,
        }


def prep_df(df):
    df = df
    df = df.reindex(
        columns=[
            "Department",
            "Name",
            "Email address",
            "Institution",
            "ID number",
            "Chapter 1",
            "Chapter 2",
            "Chapter 3",
            "Due Date #1",
            "Chapter 4",
            "Chapter 13",
            "Chapter 14",
            "Due Date #2",
            "Chapter 5",
            "Chapter 6",
            "Chapter 7",
            "Due Date #3",
            "Chapter 8",
            "Chapter 11",
            "Due Date #4",
            "Chapter 9",
            "Chapter 10",
            "Chapter 12",
            "Due Date #5",
            "Chapter 12 Skills Lab",
            "Total Hours Completed",
            "Total Hours Outstanding",
        ]
    )
    for row in df.filter(regex="Chapter ", axis=1).iterrows():
        # for each row where there may be a chapter completion date
        for k, v in row[1].items():
            # check each of the row,column values try to turn it into a date
            # row[0] is the row num, k is the column heading
            try:
                df.loc[row[0], k] = v.date()
                # df.loc[row[0], k] = datetime.date(v.strftime("%m/%d/%Y"))
            except:  # pass if turning it into a date doesn't work.
                pass

    return df
