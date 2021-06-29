# Algorithms as generators!

def bubble(data):
    n = len(data)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if data[j] > data[j + 1]:
                yield [[j, j+1], []]
                data[j], data[j + 1] = data[j + 1], data[j]
                yield [[], [j, j+1]]
            else:
                yield [[], [j, j+1]]

def insertion(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        yield[[], [i]]
        selected = False
        while j >= 0 and data[j] > key:
            if not selected:
                yield[[i], []]
            yield[[j, j+1], []]
            data[j+1] = data[j]
            yield[[], [j, j+1]]
            j -= 1
            selected = True
        yield[[j+1], []]
        data[j + 1] = key
        yield[[], [j+1]]
        