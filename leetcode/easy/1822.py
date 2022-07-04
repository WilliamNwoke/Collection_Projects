# 1822. Sign of the Product of an Array
class Solution:
    def arraySign(self, nums: List[int]) -> int:
        prod = 1
        for i in range(len(nums)):
            prod *= nums[i]
            
        if prod < 0:
            return -1
        elif prod >0:
            return 1
        
        return 0