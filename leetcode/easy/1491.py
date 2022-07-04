# 1491. Average Salary Excluding the Minimum and Maximum Salary
class Solution:
    def average(self, salary: List[int]) -> float:
        length = len(salary) -1
        salary.sort()
        sum = 0
        for i in range(1, length):
            sum +=salary[i]
        
        return sum/(length -1)
    
        
        