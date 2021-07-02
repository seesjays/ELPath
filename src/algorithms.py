# Algorithms as generators!

def bubble(data):
    n = len(data)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if data[j] > data[j + 1]:
                yield [[j, j+1], [], "Unsorted pair found"]
                data[j], data[j + 1] = data[j + 1], data[j]
                yield [[], [j, j+1], "Unsorted pair swapped"]
            else:
                yield [[], [j, j+1],"Searching for unsorted pair"]

def cocktail(data):
    swapped = True
    while swapped:
        yield [[], [], "Moving through the data from beginning to end"]
        swapped = False
        for i in range(0, len(data)-2):
            if data[i] > data[i+1]:
                yield [[i, i+1], [], "Left bar is greater than right"]
                tmp = data[i+1]
                data[i+1] = data[i]
                data[i] = tmp
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
                tmp = data[i+1]
                data[i+1] = data[i]
                data[i] = tmp
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
