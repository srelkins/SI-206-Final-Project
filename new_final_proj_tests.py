import unittest
from new_final_proj import *

class TestDatabaseTables(unittest.TestCase):
    def test_movies_table(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()

        sql = 'SELECT Title FROM Movies'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Zootopia',), result_list)
        self.assertEqual(len(result_list), 120)
        #above two statements PASS

        sql = 'SELECT ReleaseDate FROM Movies'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('2016-03-25',), result_list)
        self.assertEqual(result_list[2], ('2016-05-06',))
        self.assertEqual(result_list[-1], ('2016-01-15',))
        #above three statements PASS

        conn.close()

    def test_costumes_table(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()

        sql = 'SELECT CostumeName FROM Costume WHERE AgeGroupId = 1 '
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Princess',), result_list)
        self.assertEqual(len(result_list), 10)

        conn.close()

    def test_age_group_table(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()

        sql = 'SELECT GroupName FROM AgeGroup '
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Pets',), result_list)

        conn.close()

class TestDataAccess(unittest.TestCase):
    def test_tmdb_data_access(self):
        self.assertIn('\"page\":5,', 'cache_tmdb.json')
        #call function, assert length of response > 0

    def test_scrape_data_access(self):
        pass
        #same for scraped cache file

# class TestDataProcessing(unittest.TestCase):
#     def test_graphs_returned:
#         pass
#     def user_input_function:
#         if user_input == "movies 10":
#             self.assertEqual(len(result_list), 10)


unittest.main(verbosity=2)
