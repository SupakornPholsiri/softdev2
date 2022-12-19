import unittest 
from unittest.mock import patch

class Test(unittest.TestCase):
    @patch('builtins.input',side_effect=['2','4','1 2 3 4','1 2 3 4','1 2 3 4','1 2 3 4','5','2 2 2 2 2','2 2 2 2 2','2 2 2 2 2','2 2 2 2 2','2 2 2 2 2'])
    def test_inputfirst(self,mock_input):
        self.assertEqual(MatrixCreator().create_matrixes_from_input(),[[['1','2','3','4'],['1','2','3','4'],['1','2','3','4'],['1','2','3','4']],[['2','2','2','2','2'],['2','2','2','2','2'],['2','2','2','2','2'],['2','2','2','2','2'],['2','2','2','2','2']]])
    @patch('builtins.input',side_effect=['1','3','5 7 8','9 8 0','7 5 5'])
    def test_inputsecond(self,mock_input):
        self.assertEqual(MatrixCreator().create_matrixes_from_input(),[[['5','7','8'],['9','8','0'],['7','5','5']]])
    @patch('builtins.input',side_effect=['1','6','4 5 0 2 3 4','1 2 3 4 5 6','6 4 5 3 2 1','1 2 3 4 5 6','1 2 3 4 5 6','2 3 7 8 9 0'])
    def test_inputthird(self,mock_input):
        self.assertEqual(MatrixCreator().create_matrixes_from_input(),[[['4','5','0','2','3','4'],['1','2','3','4','5','6'],['6','4','5','3','2','1'],['1','2','3','4','5','6'],['1','2','3','4','5','6'],['2','3','7','8','9','0']]])
    @patch('builtins.input',side_effect=['2','4','1 2 3 4','1 2 3 4','1 2 3 4','1 2 3 4','5','2 2 2 2 2','2 2 2 2 2','2 2 2 2 2','2 2 2 2 2','2 2 2 2 2'])
    def test_outputfirst(self,mock_input):
        x = MatrixCreator().create_matrixes_from_input()
        self.assertEqual(Solution().display_sum_10_combi_from_all_matrix(x),"4\n10")
        

class MatrixCreator:
    def create_matrixes_from_input(self):
        matrixes = []
        n = int(input())
        while(n > 0):
            size = int(input())
            matrix = []
            for i in range(size):
                input_row = input().split(" ")
                matrix.append(input_row)
            n -= 1
            matrixes.append(matrix)
        return matrixes

class Solution:
    def display_sum_10_combi_from_all_matrix(self, matrixes):
        resultstr = ""
        for i in range(len(matrixes)):
            x = str(self.find_sum_10_combination(matrixes[i]))
            if i == len(matrixes)-1:
                resultstr += x
                return resultstr
            else:
                resultstr += x+'\n' 
    def find_sum_10_combination(self, matrix):
        return(self.count_in_rows(matrix) + self.count_in_columns(matrix))

    def count_in_rows(self,matrix):
        count = 0
        for row in range(len(matrix)):
            sum = 0
            num_of_removed = 0
            for num in matrix[row]:
                sum += int(num)
                while sum > 10:
                    sum -= int(matrix[row][num_of_removed])
                    num_of_removed += 1
                if sum == 10:
                    count += 1
        return count

    def count_in_columns(self,matrix):
        count = 0
        for column in range(len(matrix)):
            sum = 0
            num_of_removed = 0
            for row in matrix:
                sum += int(row[column])
                while sum > 10:
                    sum -= int(matrix[num_of_removed][column])
                    num_of_removed += 1
                if sum == 10:
                    count += 1
        return count
if __name__ == '__main__':
    unittest.main()