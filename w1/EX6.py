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
    def EX6(self):
        return self.display_sum_10_combi_from_all_matrix(MatrixCreator().create_matrixes_from_input())

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