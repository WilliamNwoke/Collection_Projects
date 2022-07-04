# 191. Number of 1 Bits
class Solution:
    def hammingWeight(self, n: int) -> int:
        s = str(bin(n))
        s = s[2:]
        D = {'0': 0, '1': 0}
        for i in range(0,len(s)):
            if s[i] in D: 
                D[s[i]] = D[s[i]] + 1
            else:
                D[s[i]] = 1

    
        return D['1']