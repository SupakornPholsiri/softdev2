class Solution:
    def find_duplicate(self, arr):
        duplicate = False
        occur = {}
        result = []
        for i in range(len(arr)):
            try:
                occur[arr[i]].append(i)
                duplicate = True
            except KeyError:
                occur[arr[i]] = [i]
        for dupe in occur:
            if len(occur[dupe]) > 1:
                result.append((dupe, occur[dupe]))
        return (duplicate, result)