from itertools import combinations
from functools import reduce
import pprint
import typing

def get_list_all_subsequence(list):
    return [sequence[i:j] for i, j in combinations(range(len(sequence) + 1), 2)]

#暴力解法
def max_subsequence_force(sequence):
    # 生成所有子序列
    all_subsequences = get_list_all_subsequence(sequence)
    
    # 計算所有子序列的和，並找到最大的和
    max_sum_subsequence = max(all_subsequences, key=lambda subseq: reduce(lambda x, y: x + y, subseq, 0))
    total_sum = sum(max_sum_subsequence)

    return [max_sum_subsequence, total_sum]

#分治解法
def max_subsequence_divide_conquer (sequence):

    return 

def max_subsequence_math_analytical_approach(nums: list[int]) -> int:
    n = len(nums)
    maxSum = nums[0]
    minSum = sum = 0
    for i in range(n):
        sum += nums[i]
        maxSum = max(maxSum, sum - minSum)
        minSum = min(minSum, sum)

    return maxSum
# 測試序列
sequence = [1, -2, 3, 4, -1, 2, 1, -5, 4]
result1 = max_subsequence_force(sequence)
result2 = max_subsequence_math_analytical_approach(sequence)

print("原序列:", sequence)
print("暴力 最大子序列:", result1)
print("数学分析 最大子序列:", result2)