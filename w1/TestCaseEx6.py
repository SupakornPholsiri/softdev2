import unittest
from unittest.mock import patch
from EX6 import MatrixCreator, Solution

class Test(unittest.TestCase):
    @patch('builtins.input',side_effect=['2','4','1 2 3 4','1 2 3 4','1 2 3 4','1 2 3 4','5','2 2 2 2 2','2 2 2 2 2','2 2 2 2 2','2 2 2 2 2','2 2 2 2 2'])
    def test_input_two_4x4(self,mock_input):
        self.assertEqual(MatrixCreator().create_matrixes_from_input(),[[['1','2','3','4'],['1','2','3','4'],['1','2','3','4'],['1','2','3','4']],[['2','2','2','2','2'],['2','2','2','2','2'],['2','2','2','2','2'],['2','2','2','2','2'],['2','2','2','2','2']]])

    @patch('builtins.input',side_effect=['1','3','5 7 8','9 8 0','7 5 5'])
    def test_input_3x3(self,mock_input):
        self.assertEqual(MatrixCreator().create_matrixes_from_input(),[[['5','7','8'],['9','8','0'],['7','5','5']]])

    @patch('builtins.input',side_effect=['1','6','4 5 0 2 3 4','1 2 3 4 5 6','6 4 5 3 2 1','1 2 3 4 5 6','1 2 3 4 5 6','2 3 7 8 9 0'])
    def test_input_6x6(self,mock_input):
        self.assertEqual(MatrixCreator().create_matrixes_from_input(),[[['4','5','0','2','3','4'],['1','2','3','4','5','6'],['6','4','5','3','2','1'],['1','2','3','4','5','6'],['1','2','3','4','5','6'],['2','3','7','8','9','0']]])
    
    def test_outputfirst(self):
        x = [[[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]],[[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2]]]
        self.assertEqual(Solution().display_sum_10_combi_from_all_matrix(x),"4\n10")

    def test_outputsecond(self):
        x = [[[5,7,8],[9,8,0],[7,5,5]]]
        self.assertEqual(Solution().display_sum_10_combi_from_all_matrix(x),"1")

    def test_outputthird(self):
        x = [[[4,5,0,2,3,4],[1,2,3,4,5,6],[6,4,5,3,2,1],[1,2,3,4,5,6],[1,2,3,4,5,6],[2,3,7,8,9,0]]]
        self.assertEqual(Solution().display_sum_10_combi_from_all_matrix(x),"13")

    def test_output_no_combination(self):
        x = [[[1,1,1],[1,1,1],[1,1,1]]]
        self.assertEqual(Solution().display_sum_10_combi_from_all_matrix(x),"0")

if __name__ == '__main__':
    unittest.main()