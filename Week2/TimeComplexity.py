#Bubble Sort（氣泡排序）的經典演算法
#透過比較相鄰元素的大小，將大的元素逐漸往右移動，直到最大的元素移到最右邊
#時間複雜度為 O(n^2)
def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1): #6
        # 對於每一輪，從第一個元素開始進行比較
        # 將大的元素往右移，直到最大的元素到達最右邊
        for j in range(n-1-i): #5
            if arr[j] > arr[j+1]:
                # 如果前一個元素比後一個元素大，則交換它們的位置
                arr[j], arr[j+1] = arr[j+1], arr[j]
# 測試示例
arr = [64, 34, 25, 12, 22, 11, 90]
#bubble_sort(arr)
#print("排序後的結果：", arr)

#Merge Sort（合併排序）的經典演算法
#首先檢查數列的大小，如果大小小於等於 1，則直接返回該數列（作為基本情況）。否則，將數列分成兩半，然後遞迴地對兩半進行合併排序。最後，使用 merge 函式將兩個已排序的子數列合併成一個排序好的數列。
#時間複雜度為 O(n log n)
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # 將數列分成兩半
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # 遞迴地對兩半進行合併排序
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    # 合併兩個已排序的子數列
    """ 
        merge 函式的目的是將兩個已排序的子數列合併成一個有序的數列。
        它接受兩個已排序的子數列 left 和 right，並返回一個合併後的有序數列。 
    """
    merged_arr = merge(left_half, right_half)

    return merged_arr

def merge(left, right):
    merged = []
    i = j = 0

    # 將兩個子數列按順序合併
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # 將剩餘的元素添加到合併後的數列中
    while i < len(left):
        merged.append(left[i])
        i += 1
    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged
# 測試示例
arr = [64, 34, 25, 12, 22, 11, 90]
#sorted_arr = merge_sort(arr)
#print("排序後的結果：", sorted_arr)


import random
import time

def generate_random_array(length):
    return [random.randint(1, 1000) for _ in range(length)]

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)

    return merge(left_sorted, right_sorted)

def merge(left, right):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

# 測試 bubble_sort 的執行時間
arr = generate_random_array(5000)
start_time = time.time()
bubble_sort(arr)
end_time = time.time()
execution_time = end_time - start_time
print(f"bubble_sort 執行時間：{execution_time} 秒")

# 測試 merge_sort 的執行時間
arr = generate_random_array(5000)
start_time = time.time()
merge_sort(arr)
end_time = time.time()
execution_time = end_time - start_time
print(f"merge_sort 執行時間：{execution_time} 秒")

