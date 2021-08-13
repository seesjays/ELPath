# Algorithms as generators!
# A lot of these are lifted and modified from other locations, like SO and GfG.

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
                    "message": "Pair already sorted"
                }
                
def selection(data):
    data_length = len(data)

    for i in range(data_length):
        #assume min is firt el
        j_min = i
        yield {
            "yellow": [j_min],
            "message": "New minimum found"
        }

        for j in range(i+1, data_length):
            if data[j] < data[j_min]:
                # new min
                j_min = j
                yield {
                    "yellow": [j_min],
                    "message": "New minimum found"
                }
            else:
                yield {
                    "yellow": [j_min],
                    "green": [j],
                    "message": "Searching for lower minimum"
                }

        if j_min != i:
            yield {
                "red": [j_min, i],
                "message": "Swapping the left bar with the lowest minimum"
            }
            data[i], data[j_min] = data[j_min], data[i]
            yield {
                "green": [j_min, i],
                "message": "Swap complete"
            }

#/questions/62993954/how-do-i-make-this-merge-sort-function-a-generator-python
def merge(data):
    # arr is a unique list that all levels in the recursion tree can access:

    def merge_rec(start, end):  # separate function that can take start/end indices
        if end - start > 1:
            middle = (start + end) // 2

            yield from merge_rec(start, middle)  # don't provide slice, but index range
            yield from merge_rec(middle, end)
            left = data[start:middle]
            right  = data[middle:end]

            a = 0
            b = 0
            c = start

            while a < len(left) and b < len(right):
                if left[a] < right[b]:
                    yield {
                        "red": [c],
                        "yellow": [start, end-1],
                        "message": "Sorting between yellow bars"
                    }
                    data[c] = left[a]
                    yield {
                        "green": [c],
                        "yellow": [start, end-1],
                        "message": "Sorting between yellow bars"
                    }
                    a += 1
                else:
                    yield {
                        "red": [c],
                        "yellow": [start, end-1],
                        "message": "Sorting between yellow bars"
                    }
                    data[c] = right[b]
                    yield {
                        "green": [c],
                        "yellow": [start, end-1],
                        "message": "Sorting between yellow bars"
                    }
                    b += 1
                c += 1

            while a < len(left):
                yield {
                    "red": [c],
                    "yellow": [start, end-1],
                    "message": "Adding leftover from left temp array"
                }
                data[c] = left[a]
                yield {
                    "green": [c],
                    "yellow": [start, end-1],
                    "message": "Add complete"
                }
                a += 1
                c += 1

            while b < len(right):
                yield {
                    "red": [c],
                    "yellow": [start, end-1],
                    "message": "Adding leftover from right temp array"
                }
                data[c] = right[b]
                yield {
                    "green": [c],
                    "yellow": [start, end-1],
                    "message": "Add complete"
                }
                b += 1
                c += 1

    yield from merge_rec(0, len(data))  # call inner function with start/end arguments

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

        yield {
            "yellow": [pivot_index],
            "message": "New pivot point selected"
        }

        # This loop runs till start pointer crosses
        # end pointer, and when it does we swap the
        # pivot with element on end pointer

        while intstart < intend:
            lnth = len(array)

            # Increment the start pointer till it finds an
            # element greater than  pivot
            while intstart < lnth and array[intstart] <= pivot:
                yield {
                    "red": [intstart],
                    "yellow": [pivot_index],
                    "message": "Searching for an element greater than the pivot"
                }
                intstart += 1

            if intstart < lnth:
                yield {
                    "green": [intstart],
                    "yellow": [pivot_index],
                    "message": "Found an element greater than the pivot"
                }

            # Decrement the end pointer till it finds an
            # element less than pivot
            while array[intend] > pivot:
                yield {
                    "red": [intend],
                    "yellow": [pivot_index],
                    "message": "Searching for an element smaller than the pivot"
                }
                intend -= 1

            yield {
                "green": [intend],
                "yellow": [pivot_index],
                "message": "Found an element smaller than the pivot"
            }
            # If start and end have not crossed each other,
            # swap the numbers on start and end
            if(intstart < intend):
                yield {
                    "red": [intstart, intend],
                    "yellow": [pivot_index],
                    "message": "Swapping the smaller and greater elements"
                }
                array[intstart], array[intend] = array[intend], array[intstart]
                yield {
                    "green": [intstart, intend],
                    "yellow": [pivot_index],
                    "message": "Swap complete"
                }

        # Swap pivot element with element on end pointer.
        # This puts pivot on its correct sorted place.
        yield {
            "red": [intend, pivot_index],
            "message": "Placing pivot where the last smaller element was"
        }
        array[intend], array[pivot_index] = array[pivot_index], array[intend]
        yield {
            "green": [intend, pivot_index],
            "message": "Pivot placed"
        }
        # Returning end pointer to divide the array into 2
        p = intend
        
        
        # Sort elements before partition
        # and after partition
        
        yield from quick_sort(start, p - 1, array)
        yield from quick_sort(p + 1, end, array)

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
                    "red": [i, i+1],
                    "message": "Left bar is greater than right"
                }
                data[i], data[i+1] = data[i+1], data[i]
                swapped = True
                yield {
                    "green": [i, i+1],
                    "message": "Swapped bars"
                }
            else:
                yield {
                    "yellow": [i, i+1],
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
                    "red": [i, i+1],
                    "message": "Left bar is greater than right"
                }
                data[i], data[i+1] = data[i+1], data[i]
                swapped = True
                yield {
                    "green": [i, i+1],
                    "message": "Swapped bars"
                }
            else:
                yield {
                    "yellow": [i, i+1],
                    "message": "Bars already ordered"
                }

    yield

def insertion(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        yield {
            "yellow": [i],
            "message": "Checking bar before this one for a greater value"
        }
        selected = False
        while j >= 0 and data[j] > key:
            if not selected:
                yield {
                    "red": [i],
                    "message": "Bar before this is greater, saving the smaller bar"
                }

            yield {
                "red": [j, j+1],
                "message": "Moving the left bar forward"
            }
            data[j+1] = data[j]
            yield {
                "green": [j, j+1],
                "message": "Move complete"
            }
            j -= 1
            selected = True
        yield {
            "yellow": [j+1],
            "message": "Replacing this bar with the smaller one from earlier"
        }
        data[j + 1] = key
        yield {
            "green": [j+1],
            "message": "Replacement complete"
        }
