# Algorithms as generators!

def bubble(data):
    n = len(data)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if data[j] > data[j + 1]:
                yield {
                    "highlight": [j, j+1],
                    "message": "Unsorted pair found"
                }
                data[j], data[j + 1] = data[j + 1], data[j]
                yield {
                    "highlight-special": [j, j+1],
                    "message": "Unsorted pair swapped"
                }
            else:
                yield {
                    "highlight-special": [j, j+1],
                    "message": "Pair already sorted"
                }
                
def selection(data):
    data_length = len(data)

    for i in range(data_length):
        #assume min is firt el
        j_min = i
        yield {
            "selected": [j_min],
            "message": "New minimum found"
        }

        for j in range(i+1, data_length):
            if data[j] < data[j_min]:
                # new min
                j_min = j
                yield {
                    "selected": [j_min],
                    "message": "New minimum found"
                }
            else:
                yield {
                    "selected": [j_min],
                    "highlight-special": [j],
                    "message": "Searching for lower minimum"
                }

        if j_min != i:
            yield {
                "highlight": [j_min, i],
                "message": "Swapping the left bar with the lowest minimum"
            }
            data[i], data[j_min] = data[j_min], data[i]
            yield {
                "highlight-special": [j_min, i],
                "message": "Swap complete"
            }

#/questions/62993954/how-do-i-make-this-merge-sort-function-a-generator-python
def merge(arr):
    # arr is a unique list that all levels in the recursion tree can access:

    def merge_rec(start, end):  # separate function that can take start/end indices
        if end - start > 1:
            middle = (start + end) // 2

            yield from merge_rec(start, middle)  # don't provide slice, but index range
            yield from merge_rec(middle, end)
            left = arr[start:middle]
            right  = arr[middle:end]

            a = 0
            b = 0
            c = start

            while a < len(left) and b < len(right):
                if left[a] < right[b]:
                    yield {
                        "highlight": [c],
                        "selected": [start, end-1],
                        "message": "Sorting between yellow bars"
                    }
                    arr[c] = left[a]
                    yield {
                        "highlight-special": [c],
                        "selected": [start, end-1],
                        "message": "Sorting between yellow bars"
                    }
                    a += 1
                else:
                    yield {
                        "highlight": [c],
                        "selected": [start, end-1],
                        "message": "Sorting between yellow bars"
                    }
                    arr[c] = right[b]
                    yield {
                        "highlight-special": [c],
                        "selected": [start, end-1],
                        "message": "Sorting between yellow bars"
                    }
                    b += 1
                c += 1

            while a < len(left):
                yield {
                    "highlight": [c],
                    "selected": [start, end-1],
                    "message": "Adding leftover from left temp array"
                }
                arr[c] = left[a]
                yield {
                    "highlight-special": [c],
                    "selected": [start, end-1],
                    "message": "Add complete"
                }
                a += 1
                c += 1

            while b < len(right):
                yield {
                    "highlight": [c],
                    "selected": [start, end-1],
                    "message": "Adding leftover from right temp array"
                }
                arr[c] = right[b]
                yield {
                    "highlight-special": [c],
                    "selected": [start, end-1],
                    "message": "Add complete"
                }
                b += 1
                c += 1
            print(arr, start, end)

    yield from merge_rec(0, len(arr))  # call inner function with start/end arguments



def cocktail(data):
    swapped = True
    while swapped:
        yield {
            "message": "Moving through the data from beginning to end"
        }
        swapped = False
        for i in range(0, len(data)-2):
            if data[i] > data[i+1]:
                yield {
                    "highlight": [i, i+1],
                    "message": "Left bar is greater than right"
                }
                data[i], data[i+1] = data[i+1], data[i]
                swapped = True
                yield {
                    "highlight-special": [i, i+1],
                    "message": "Swapped bars"
                }
            else:
                yield {
                    "selected": [i, i+1],
                    "message": "Bars already ordered"
                }

        if not swapped:
            break

        yield {
            "message": "Moving from end to beginning now"
        }
        
        swapped = False
        for i in range(len(data)-2, 0, -1):
            if data[i] > data[i+1]:
                yield {
                    "highlight": [i, i+1],
                    "message": "Left bar is greater than right"
                }
                data[i], data[i+1] = data[i+1], data[i]
                swapped = True
                yield {
                    "highlight-special": [i, i+1],
                    "message": "Swapped bars"
                }
            else:
                yield {
                    "selected": [i, i+1],
                    "message": "Bars already ordered"
                }

    yield

def insertion(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        yield {
            "selected": [i],
            "message": "Checking bar before this one for a greater value"
        }
        selected = False
        while j >= 0 and data[j] > key:
            if not selected:
                yield {
                    "highlight": [i],
                    "message": "Bar before this is greater, saving the smaller bar"
                }

            yield {
                "highlight": [j, j+1],
                "message": "Moving the left bar forward"
            }
            data[j+1] = data[j]
            yield {
                "highlight-special": [j, j+1],
                "message": "Move complete"
            }
            j -= 1
            selected = True
        yield {
            "selected": [j+1],
            "message": "Replacing this bar with the smaller one from earlier"
        }
        data[j + 1] = key
        yield {
            "highlight-special": [j+1],
            "message": "Replacement complete"
        }
