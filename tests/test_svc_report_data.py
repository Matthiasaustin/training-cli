import unittest
from pathlib import Path
import pandas as pd

from training.services import svc_report_data as data


class TestData(unittest.TestCase):
    def setUp(self):
        # pandas dataframe with example data

        #save csv from df to test import
        pass

    def test_get_month(self):
        """
        Test that the regex pulls the correct month.
        """
        test1 = '/home/users/matthias/Documents/code/training-cli/data/completion-february_chapter_03-20210307_0204-comma_separated.csv'
        test2 = 'C:\\Users\\maustin\\Documents\\!Matthias\\code\\training-cli\\data\\completion-march_chapter_09-20210307_0204-comma_separated.csv'
        test3 = Path(test1)
        test4 = Path(test2)

        result1 = data.get_month(test1)
        self.assertEqual(result1, 'february')
        result2 = data.get_month(test2)
        self.assertEqual(result2, 'march')
        result3 = data.get_month(test3)
        self.assertEqual(result3, 'february')
        result4 = data.get_month(test4)
        self.assertEqual(result4, 'march')


if __name__ == '__main__':
    unittest.main()
