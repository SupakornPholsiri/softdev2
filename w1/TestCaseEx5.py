import unittest
from EX5 import Solution

class Ex5_test_cases(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(sorted(Solution().find_all_3_combination([0, -1, 2, -3, 1, -2])), sorted([(-2, 0, 2), (-3, 1, 2), (-1, 0, 1)]))

    def test_no_combination(self):
        self.assertTrue(len(Solution().find_all_3_combination([0, 6, 7, -3, 1, 4])) == 0)

    def test_not_enough_element(self):
        self.assertTrue(len(Solution().find_all_3_combination([0, 6])) == 0)

    def test_no_element(self):
        self.assertTrue(len(Solution().find_all_3_combination([])) == 0)

if __name__ == "__main__":
    unittest.main()