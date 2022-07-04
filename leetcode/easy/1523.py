# 1523. Count Odd Numbers in an Interval Range
class Solution:
    def countOdds(self, low: int, high: int) -> int:
        odd = (low%2 + high%2 + high - low)//2
        return odd