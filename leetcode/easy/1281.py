# 1281. Subtract the Product and Sum of Digits of an Integer
class Solution:
    def subtractProductAndSum(self, n: int) -> int:
        summ = 0
        prod =1
        s = str(n)
        for i in range(len(s)):
            summ +=int(s[i])
            prod *=int(s[i])
            
        return prod - summ