# 1502. Can Make Arithmetic Progression From Sequence
class Solution:
    def canMakeArithmeticProgression(self, arr: List[int]) -> bool:
        if len(arr) < 3:
            return True
        arr.sort()
        preD =0
        currD =0
        
        for i in range(2,len(arr)):
            preD = arr[i-1] - arr[i-2]
            currD = arr[i] - arr[i-1]
            if currD != preD:
                return False
        return True