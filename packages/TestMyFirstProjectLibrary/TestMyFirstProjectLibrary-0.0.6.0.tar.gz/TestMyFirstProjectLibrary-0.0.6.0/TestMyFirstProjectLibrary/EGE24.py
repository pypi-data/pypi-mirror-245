class Find:
    def Longest_char(file,char):
        s = file.readline()
        max = 0
        for i in range(len(s) + 1):
            if char * i in s:
                max = i
        return max

    def LongestHoatic_str(file,string):
        s = file.readline()
        max = 0
        k = 0
        for i in range(len(s)):
            if s[i] in string:
                k += 1
                if k > max:
                    max = k
            else:
                k = 0
        return max

    def TheMostUsed_char(string):
        max = -1
        char = ''
        for c in (set(string)):
            if(string.count(c)>max):
                max = string.count(c)
                char = c
        return max,char
