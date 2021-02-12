import pandas as pd
from datetime import datetime

class CourseReporter():
    def __init__(self):
        self.static_headers = ['ID', 'Name', 'ID number',
                              'Email address', 'Department',
                              'Institution', 'Course complete',
                              'Chapter', 'Month']
        self.course_hours = {
            "chapter_01": 2.5,
            "chapter_02": 2,
            "chapter_03": 2.5,
            "chapter_04": 4,
            "chapter_05": 4,
            "chapter_06": 1.5,
            "chapter_07": 2,
            "chapter_08": 4,
            "chapter_09": 4,
            "chapter_10": 2.5,
            "chapter_11": 2.5,
            "chapter_12": 6,
            "chapter_13": 1.5,
            "chapter_14": 2,
        }

    def make_report(self):
        pass
