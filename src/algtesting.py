from random import randint

testvalset = [i for i in range(50)]

def bubble(data):
    n = len(data)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]

def selection(data):
    data_length = len(data)

    for i in range(data_length):
        #assume min is firt el
        j_min = i

        for j in range(i+1, data_length):
            if data[j] < data[j_min]:
                # new min
                j_min = j
        if j_min != i:
            data[i], data[j_min] = data[j_min], data[i]

def cocktail(data):
    swapped = True
    while swapped:
        swapped = False
        for i in range(0, len(data)-2):
            if data[i] > data[i+1]:
                tmp = data[i+1]
                data[i+1] = data[i]
                data[i] = tmp
                swapped = True
        if not swapped:
            break
        swapped = False
        for i in range(len(data)-2, 0, -1):
            if data[i] > data[i+1]:
                tmp = data[i+1]
                data[i+1] = data[i]
                data[i] = tmp
                swapped = True

def merge(data):
    if len(data) > 1:
         # Finding the mid of the array
        mid = len(data)//2
 
        # Dividing the array elements
        L = data[:mid]
 
        # into 2 halves
        R = data[mid:]
 
        # Sorting the first half
        merge(L)
 
        # Sorting the second half
        merge(R)
 
        i = j = k = 0
 
        # Copy data to temp dataays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                data[k] = L[i]
                i += 1
            else:
                data[k] = R[j]
                j += 1
            k += 1
 
        # Checking if any element was left
        while i < len(L):
            data[k] = L[i]
            i += 1
            k += 1
 
        while j < len(R):
            data[k] = R[j]
            j += 1
            k += 1

def merge_sort(arr):
    # arr is a unique list that all levels in the recursion tree can access:

    def mergeSortRec(start, end):  # separate function that can take start/end indices
        if end - start > 1:
            middle = (start + end) // 2

            yield from mergeSortRec(start, middle)  # don't provide slice, but index range
            yield from mergeSortRec(middle, end)
            left = arr[start:middle]
            right  = arr[middle:end]

            a = 0
            b = 0
            c = start

            while a < len(left) and b < len(right):
                if left[a] < right[b]:
                    arr[c] = left[a]
                    a += 1
                else:
                    arr[c] = right[b]
                    b += 1
                c += 1

            while a < len(left):
                arr[c] = left[a]
                a += 1
                c += 1

            while b < len(right):
                arr[c] = right[b]
                b += 1
                c += 1
            print(arr, start, end)
            
            yield {
                "highlight": [start, end],
                "message": "lmao"
            }

    yield from mergeSortRec(0, len(arr)) 


for x in merge_sort(testvalset):
    print(x)