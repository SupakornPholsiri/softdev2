import unittest
from EX4 import Solution

class EX4Testcase(unittest.TestCase):
    def test_have_duplicate(self):
        solution = Solution()
        self.assertTrue(solution.find_duplicate([1,1,1,1,1,1]), (True, [(1, (0,1,2,3,4,5))] ))
        self.assertTrue(solution.find_duplicate([1,2,1,1,1,1]), (True, [(1, (0,2,3,4,5))] ))
        self.assertTrue(solution.find_duplicate([1,2,3,2,3,1]), (True, [(1, (0,5)), (2, (1,3)), (3, (2,4))] ))

    def test_no_duplicate(self):
        self.assertEqual(Solution().find_duplicate([1,0,2,6,4,3]), (False, []))
    
    def test_single_element(self):
        self.assertEqual(Solution().find_duplicate([1]), (False, []))

    def test_empty_list(self):
        self.assertEqual(Solution().find_duplicate([]), (False, []))

if __name__ == "__main__":
    unittest.main()