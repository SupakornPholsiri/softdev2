class Solution:
    def find_all_3_combination(self,array):
        result = []
        array.sort()
        for i in range(len(array)-1):
            x = array[i]
            diff = 0 - x
            left = i+1
            right = len(array)-1
            while(left != right):
                sum = array[left] + array[right]
                if sum == diff:
                    result.append((array[i],array[left],array[right]))
                    left += 1
                elif sum < diff: left += 1
                elif sum > diff: right -= 1
        return result