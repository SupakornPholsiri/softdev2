import unittest
from unittest.mock import patch,mock_open
from EX7 import InputStruct, Solution

class FakeInputStruct:
    def __init__(self, filename):
        self.array_length = 16
        self.c1 = 200
        self.c2 = -10
        self.num_array = [12,70,1,999,50,20,1000,150,300,200,90,900,40,140,130,30]

class FakeInputStructWithNotEnoughElements:
    def __init__(self, filename):
        self.array_length = 6
        self.c1 = 200
        self.c2 = -10
        self.num_array = [12,70,1,999,50,20]

class FakeInputStructWithNoSolution:
    def __init__(self, filename):
        self.array_length = 16
        self.c1 = 100
        self.c2 = -10
        self.num_array = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

class Test(unittest.TestCase):
    Test1 ="16 200 -10\n12\n70\n1\n999\n50\n20\n1000\n150\n300\n200\n90\n900\n40\n140\n130\n30"
    Test2 ="6 200 -10\n12\n70\n1\n999\n50\n20"
    Test3 ="8 100 -10\n0\n1\n2\n3\n4\n5\n6\n7"

    @patch('builtins.open',new=mock_open(read_data=Test1))
    def test_inputfirst(self):
        x = InputStruct('/dev/null')
        result = x.num_array
        self.assertEqual(result,[12,70,1,999,50,20,1000,150,300,200,90,900,40,140,130,30])

    @patch('builtins.open',new=mock_open(read_data=Test2))
    def test_inputsecond(self):
        x = InputStruct('/dev/null')
        result = x.num_array
        self.assertEqual(result,[12,70,1,999,50,20])

    @patch('builtins.open',new=mock_open(read_data=Test3))
    def test_inputthird(self):
        x = InputStruct('/dev/null')
        result = x.num_array
        self.assertEqual(result,[0,1,2,3,4,5,6,7])

    @patch('__main__.InputStruct', new=FakeInputStruct)
    def test_outputfirst(self):
        y = Solution()
        self.assertEqual(y.EX7(InputStruct('/dev/null')),(50,150,20,70,90,40,130,30))

    @patch('__main__.InputStruct', new=FakeInputStructWithNotEnoughElements) 
    def test_not_enough_elements(self):
        y = Solution()
        self.assertIsNone(y.EX7(InputStruct('/dev/null')))

    @patch('__main__.InputStruct', new=FakeInputStructWithNoSolution)
    def test_no_solution(self):
        y = Solution()
        self.assertIsNone(y.EX7(InputStruct('/dev/null')))

if __name__ == '__main__':
    unittest.main()