from random import randint



testvalset = [randint(0, 50) for i in range(50)]

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

     
# The main function that implements QuickSort
def quick_sort(start, end, array):
     
    if (start < end):
        ###
        intstart = start
        intend = end
        # p is partitioning index, array[p]
        # is at right place
        # Initializing pivot's index to start
        pivot_index = intstart
        pivot = array[pivot_index]

        # This loop runs till start pointer crosses
        # end pointer, and when it does we swap the
        # pivot with element on end pointer
        while intstart < intend:

            # Increment the start pointer till it finds an
            # element greater than  pivot
            while intstart < len(array) and array[intstart] <= pivot:
                intstart += 1

            # Decrement the end pointer till it finds an
            # element less than pivot
            while array[intend] > pivot:
                intend -= 1

            # If start and end have not crossed each other,
            # swap the numbers on start and end
            if(intstart < intend):
                array[intstart], array[intend] = array[intend], array[intstart]

        # Swap pivot element with element on end pointer.
        # This puts pivot on its correct sorted place.
        array[intend], array[pivot_index] = array[pivot_index], array[intend]

        # Returning end pointer to divide the array into 2
        p = intend
        yield p, array
        # Sort elements before partition
        # and after partition
        yield from quick_sort(start, p - 1, array)
        yield from quick_sort(p + 1, end, array)
        
print(testvalset)
dar = testvalset.copy()
dar.sort()
print(dar)

for x in quick_sort(0, len(testvalset)-1, testvalset):
    print(x)

print(testvalset)
if dar == testvalset:
    print("sorted")
    