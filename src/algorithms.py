# Algorithms as generators!

def bubble(data):
    n = len(data)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if data[j] > data[j + 1]:
                yield {
                    "red": [j, j+1],
                    "message": "Unsorted pair found"
                }
                data[j], data[j + 1] = data[j + 1], data[j]
                yield {
                    "green": [j, j+1],
                    "message": "Unsorted pair swapped"
                }
            else:
                yield {
                    "green": [j, j+1],
                    "message": "Searching for unsorted pair"
                }
                
def selection(data):
    data_length = len(data)

    for i in range(data_length):
        #assume min is firt el
        j_min = i
        yield [[], [j_min], "Moving forward, assuming this is the minimum"]

        for j in range(i+1, data_length):
            if data[j] < data[j_min]:
                # new min
                j_min = j
                yield [[j_min], [], "New minimum found"]
            else:
                yield [[j_min], [j], "Searching for new minimum"]

        if j_min != i:
            yield [[j_min, i], [], "Replacing the left bar with the new minimum"]
            data[i], data[j_min] = data[j_min], data[i]
            yield [[], [j_min, i], "Replacement complete"]


def merge(data):
    if len(data) > 1:
         # Finding the midpoint of the array
        mid = len(data)//2
 
        # Dividing the array elements
        L = data[:mid]
 
        # into 2 halves
        R = data[mid:]

        # Sorting the first half
        yield from merge(L)
 
        # Sorting the second half
        yield from merge(R)
 
        i = j = k = 0
 
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            yield [[i, j], [k], ""]
            if L[i] < R[j]:
                data[k] = L[i]
                i += 1
                yield [[], [i, j, k], ""]
            else:
                data[k] = R[j]
                j += 1
                yield [[], [i, j, k], ""]
            k += 1
 
        # Checking if any element was left
        while i < len(L):
            yield [[i, k], [], ""]
            data[k] = L[i]
            yield [[i], [k], ""]
            i += 1
            k += 1
 
        while j < len(R):
            yield [[j, k], [], ""]
            data[k] = R[j]
            yield [[j], [k], ""]
            j += 1
            k += 1


def cocktail(data):
    swapped = True
    while swapped:
        yield [[], [], "Moving through the data from beginning to end"]
        swapped = False
        for i in range(0, len(data)-2):
            if data[i] > data[i+1]:
                yield [[i, i+1], [], "Left bar is greater than right"]
                data[i], data[i+1] = data[i+1], data[i]
                swapped = True
                yield [[], [i, i+1], "Swapped bars"]
            else:
                yield [[], [i, i+1], "Bars already ordered"]

        if not swapped:
            break
        
        yield [[], [], "Moving from end to beginning now"]
        
        swapped = False
        for i in range(len(data)-2, 0, -1):
            if data[i] > data[i+1]:
                yield [[i, i+1], [], "Left bar is greater than right"]
                data[i], data[i+1] = data[i+1], data[i]
                swapped = True
                yield [[], [i, i+1], "Swapped bars"]
            else:
                yield [[], [i, i+1], "Bars already ordered"]

    yield

def insertion(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        yield[[], [i], "Checking bar before this one for a greater value"]
        selected = False
        while j >= 0 and data[j] > key:
            if not selected:
                yield[[i], [], "Bar before this is greater, saving the smaller bar"]
            yield[[j, j+1], [], "Moving the left bar forward"]
            data[j+1] = data[j]
            yield[[], [j, j+1], "Moved the left bar forward"]
            j -= 1
            selected = True
        yield[[j+1], [], "Replacing this bar with the smaller one from earlier"]
        data[j + 1] = key
        yield[[], [j+1], "Replacement complete"]

