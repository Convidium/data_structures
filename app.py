def insertion_sort(A):
    for j in range(1, len(A)):
        value = A[j]
        i=j-1
        while i >= 0 and A[i] > value:
            A[i+1] = A[i]
            i = i - 1
        A[i + 1] = value
        
def merge_sort(A):
    if len(A) <= 1:
        return A

    mid = len(A) // 2
    left = merge_sort(A[:mid])
    right = merge_sort(A[mid:])
    
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] >= right[j]:
            result.append(right[j])
            j += 1
        else:
            result.append(left[i])
            i += 1
            
    result.extend(left[i:])
    result.extend(right[j:])
    return result
        
arr = [7,5,3,4,5,6,7,8]
print(merge_sort(arr))