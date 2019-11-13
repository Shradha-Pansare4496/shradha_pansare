"""
Name : Shradha .M. Pansare
CWID : 10449587
"""

import unittest
import os
from HW11_Shradha_Pansare import Repository


class TestCase(unittest.TestCase):
    def test_db(self):
        wdir = '/Users/shradhapansare/Desktop/test_repository'
        Stevens = Repository(wdir)
        wdir = os.getcwd()
        db_path = os.path.join(wdir, "stevens files")
        Stevens = Repository(wdir)

        instructor_db_result = list()

        for row in Repository.instructor_table_db:
            instructor_db_result.append(row)
            self.assertEqual(instructor_db_result, [('98762', 'Hawking, S', 'CS', 'CS 501', 1),
                                                     ('98762', 'Hawking, S', 'CS', 'CS 546', 1),
                                                     ('98762', 'Hawking, S', 'CS', 'CS 570', 1),
                                                     ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1),
                                                     ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4),
                                                     ('98764', 'Cohen, R', 'SFEN', 'CS 546', 1)])

if __name__ == '__main__':
    
    unittest.main(exit=False, verbosity=2)
