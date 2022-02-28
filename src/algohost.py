from random import randint


class AlgorithmHost:
    def __init__(self, algorithm="Quick Sort"):
        self.data_set_size = 30

        self.step_counter = 0

        self.data_x = [i for i in range(self.data_set_size)]
        self.data_original = []
        self.data_y = []

        self.alg_list = {
            "Quick Sort": (lambda: self.quick_sort(0, self.data_set_size-1, self.data_y)),
            "Merge Sort": (lambda: self.merge(self.data_y)),
            "Bubble Sort": (lambda: self.regbubble(self.data_y)),
            "Optimized Bubble Sort": (lambda: self.bubble(self.data_y)),
            "Insertion Sort": (lambda: self.insertion(self.data_y)),
            "Selection Sort": (lambda: self.selection(self.data_y)),
            "Cocktail Sort": (lambda: self.cocktail(self.data_y)),
        }
        self.alg_name = algorithm
        self.current_algorithm = self.alg_list[self.alg_name]()

        self.set_random_data()

    def set_algorithm(self, name):
        self.alg_name = name
        self.step_counter = 0
        self.current_algorithm = self.alg_list[name]()

    def set_random_data(self):
        self.step_counter = 0
        self.data_y = [randint(1, self.data_set_size)
                       for i in range(self.data_set_size)]
        self.data_original = self.data_y.copy()
        self.current_algorithm = self.alg_list[self.alg_name]()

    def original_data(self):
        self.step_counter = 0
        self.data_y = self.data_original.copy()
        self.current_algorithm = self.alg_list[self.alg_name]()

    def change_data_len(self, changeamnt):
        self.step_counter = 0

        if (changeamnt < 0 and self.data_set_size - abs(changeamnt) < 5) or (changeamnt > 0 and self.data_set_size + abs(changeamnt) > 100):
            return

        self.data_set_size += changeamnt

        self.data_x = [i for i in range(self.data_set_size)]
        self.data_y = [randint(1, self.data_set_size)
                       for i in range(self.data_set_size)]

        self.data_original = self.data_y.copy()
        self.current_algorithm = self.alg_list[self.alg_name]()

    def next_step(self):
        try:
            self.step_counter += 1
            return next(self.current_algorithm)
        except StopIteration:
            self.step_counter -= 1
            return False

    # Algorithms

    def regbubble(self, data):
        n = len(data)
        changemade = False
        while not changemade:
            changemade = True
            for i in range(n-1):
                j = i + 1
                if data[j] < data[i]:
                    yield {
                        "red": [i, j],
                        "message": "Unsorted pair found"
                    }
                    data[i], data[j] = data[j], data[i]
                    yield {
                        "green": [i, j],
                        "message": "Unsorted pair swapped"
                    }
                    changemade = False
                else:
                    yield {
                        "green": [i, j],
                        "message": "Pair already sorted"
                    }

    def bubble(self, data):
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

    def selection(self, data):
        data_length = len(data)

        for i in range(data_length):
            # assume min is firt el
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

    # /questions/62993954/how-do-i-make-this-merge-sort-function-a-generator-python
    def merge(self, data):
        # arr is a unique list that all levels in the recursion tree can access:

        def merge_rec(start, end):  # separate function that can take start/end indices
            if end - start > 1:
                middle = (start + end) // 2

                # don't provide slice, but index range
                yield from merge_rec(start, middle)
                yield from merge_rec(middle, end)
                left = data[start:middle]
                right = data[middle:end]

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

        # call inner function with start/end arguments
        yield from merge_rec(0, len(data))

    # The main function that implements QuickSort
    def quick_sort(self, start, end, array):
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

            yield from self.quick_sort(start, p - 1, array)
            yield from self.quick_sort(p + 1, end, array)

    def cocktail(self, data):
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

    def insertion(self, data):
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
