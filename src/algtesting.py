from random import randint

testvalset = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

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

merge(testvalset)

print((testvalset))