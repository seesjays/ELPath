from random import randint

testvalset = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

def bubble(data):
    n = len(data)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]


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

cocktail(testvalset)

print((testvalset))