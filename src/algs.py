from random import randint

testvalset = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

def bubble(data):
    n = len(data)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]

bubble(testvalset)

print((testvalset))