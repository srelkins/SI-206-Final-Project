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
        self.assertEqual(("Ride Along 2",), result_list[-1])
        self.assertEqual(len(result_list), 120)
        #above statements PASS

        sql = 'SELECT ReleaseDate FROM Movies'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('2016-03-25',), result_list)
        self.assertEqual(result_list[2], ('2016-05-06',))
        self.assertEqual(result_list[-1], ('2016-01-15',))
        #above statements PASS

        sql = 'SELECT VoteCount FROM Movies'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn((533,), result_list)
        self.assertEqual(result_list[2], (9294,))
        self.assertEqual(result_list[-1], (688,))
        #above three statements PASS

        conn.close()

    def test_costumes_table(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()

        sql = 'SELECT CostumeName FROM Costumes WHERE AgeGroupId = 1 '
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Princess',), result_list)
        self.assertEqual(result_list[-1], ("Spiderman",))
        self.assertEqual(len(result_list), 10)
        #above statements PASS

        sql2 = 'SELECT CostumeName FROM Costumes WHERE AgeGroupId = 3 '
        results2 = cur.execute(sql2)
        result_list2 = results.fetchall()
        self.assertIn(("Vampire",), result_list2)
        self.assertEqual(result_list2[1], ("Pirate",))
        self.assertEqual(len(result_list2), 10)
        #above statements PASS

        conn.close()

    def test_age_group_table(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()

        sql = 'SELECT GroupName FROM AgeGroup '
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Pets',), result_list)
        self.assertIn(('Adults 35+',), result_list)
        self.assertEqual(len(result_list), 4)
        #above statements PASS

        conn.close()

# class TestDataAccess(unittest.TestCase):
#     def test_tmdb_data_access(self):
#         pass
#         #self.assertIn('\"page\":5,', cache_tmdb.json)
#         #call function, assert length of response > 0
#
#     def test_scrape_data_access(self):
#         pass
#         # scrape_halloween_costumes()
#         # self.assertIn("Pets", costume_text)
#         #same for scraped cache file
#
# class TestDataProcessing(unittest.TestCase):
#     #following test cases are not running?
#     def test_costume_data_returned(self):
#
#         if user_input == "costumes pets":
#             self.assertTrue(len(pets_costumes) > 10)
#             self.assertIn("Superman", pets_costumes)
#         elif user_input == "costumes children":
#             self.assertIn("Princess", childrens_costumes)
#             self.assertEqual(len(childrens_costumes), 10)
#         # elif user_input == "movies 15":
#         #     self.assertEqual(len(result_list), 15)
#         elif user_input == "graph top 10 movies popularity":
#             self.assertIn("Deadpool", movie_titles)
#
#             self.assertIn("sdklfjsd;lf", movie_titles)

unittest.main(verbosity=2)
