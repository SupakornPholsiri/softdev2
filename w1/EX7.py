class InputStruct:
    def __init__(self, filename):
        infile = open(filename, 'r')
        line = (infile.readlines())
        lstfirstinput = line[0].split()

        self.array_length = int(lstfirstinput[0])
        self.c1 = int(lstfirstinput[1])
        self.c2 = int(lstfirstinput[2])
        self.num_array = self.create_array_from_file(line)
        
        infile.close()

    def create_array_from_file(self, lines):
        lstinput = []
        for i in range(self.array_length):
            lstinput.append(int(lines[i+1]))
        set(lstinput)
        return list(lstinput)

class Solution:
    def twoSum(self, nums, target, to_skip = []):
        d = dict()
        for i in range(len(nums)) :
            if nums[i] in to_skip:
                continue
            if nums[i] in d :
                return (nums[i],nums[d[nums[i]]])
            d[target-nums[i]] = i

    def twoDiff(self, nums, target, to_skip):
        d = dict()
        if target < 0:
            multi = -1
        else:
            multi = 1
        for i in range(len(nums)) :
            if to_skip[nums[i]] == 2:
                continue
            if nums[i] in d and to_skip[nums[i]] == 0:
                if multi*nums[i] <= multi*nums[d[nums[i]]]:
                    return (nums[i],nums[d[nums[i]]])
                return (nums[d[nums[i]]],nums[i])
            d[target+nums[i]] = i
            d[nums[i]-target] = i
            
    def EX7(self, inputStruct):
        solution_found = False

        x1_x2_skip = []
        skip_dict = {num: 0 for num in inputStruct.num_array}
        skip_dict[min(inputStruct.num_array)] = 1
        skip_dict[max(inputStruct.num_array)] = 1

        while not solution_found:
            x3_x4_skip = skip_dict.copy()
            x6_x8_skip = skip_dict.copy()
            x5_x7_skip = skip_dict.copy()
            potential_x1_x2 = self.twoSum(inputStruct.num_array, inputStruct.c1, x1_x2_skip)
            if potential_x1_x2:
                x1, x2 = potential_x1_x2
                x1_x2_skip.append(x1)
                x1_x2_skip.append(x2)
                x3_x4_skip[x1] = 2
                x3_x4_skip[x2] = 2
                x6_x8_skip[x1] = 2
                x6_x8_skip[x2] = 2

                while not solution_found:
                    potential_x3_x4 = self.twoDiff(inputStruct.num_array, x1, x3_x4_skip)
                    if potential_x3_x4:
                        x3, x4 = potential_x3_x4
                        x3_x4_skip[x3] += 1
                        x3_x4_skip[x4] += 1
                        x6_x8_skip[x3] = 2
                        x6_x8_skip[x4] = 2
                        x5_x7_skip = x6_x8_skip.copy()

                        while not solution_found:
                            potential_x6_x8 = self.twoDiff(inputStruct.num_array, inputStruct.c2, x6_x8_skip)
                            if potential_x6_x8:
                                x6, x8 = potential_x6_x8
                                x6_x8_skip[x6] += 1
                                x6_x8_skip[x8] += 1
                                x5_x7_skip[x6] = 2
                                x5_x7_skip[x8] = 2

                                potential_x5_x7 = self.twoDiff(inputStruct.num_array, x6, x5_x7_skip)
                                if potential_x5_x7:
                                    x5, x7 = potential_x5_x7
                                    solution_found = True
                                    return (x1, x2, x3, x4, x5, x6, x7, x8)
                                else:
                                    x5_x7_skip[x6] = 0
                                    x5_x7_skip[x8] = 0
                                    continue
                            else:
                                x6_x8_skip[x3] = 0
                                x6_x8_skip[x4] = 0
                                break


                    else:
                        potential_x3_x4 = self.twoDiff(inputStruct.num_array, x2, x3_x4_skip)
                        if potential_x3_x4:
                            x3, x4 = potential_x3_x4
                            x3_x4_skip[x3] += 1
                            x3_x4_skip[x4] += 1
                            x6_x8_skip[x3] = 2
                            x6_x8_skip[x4] = 2
                            x5_x7_skip = x6_x8_skip.copy()
                            x1, x2 = x2, x1

                            while not solution_found:
                                potential_x6_x8 = self.twoDiff(inputStruct.num_array, inputStruct.c2, x6_x8_skip)
                                if potential_x6_x8:
                                    x6, x8 = potential_x6_x8
                                    x6_x8_skip[x6] += 1
                                    x6_x8_skip[x8] += 1
                                    x5_x7_skip[x6] = 2
                                    x5_x7_skip[x8] = 2

                                    potential_x5_x7 = self.twoDiff(inputStruct.num_array, x6, x5_x7_skip)
                                    if potential_x5_x7:
                                        x5, x7 = potential_x5_x7
                                        
                                        return (x1, x2, x3, x4, x5, x6, x7, x8)
                                    else:
                                        x5_x7_skip[x6] = 0
                                        x5_x7_skip[x8] = 0
                                        continue
                                else:
                                    x6_x8_skip[x3] = 0
                                    x6_x8_skip[x4] = 0
                                    break
                        else:
                            break
                
            else:    
                break