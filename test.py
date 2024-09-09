from collections import deque
"""
Помимо классисческой проверки на четность через проверку остатка от деления на 2
существует проверка на последний бит в двоичной репрезентации числа
последний бит в четном двоичном числе всегда 0
"""
def is_even(number: int):
    binary = bin(number)
    last_bit = binary[-1]
    if last_bit == '0':
        return True
    else:
        return False

"""
Кольцевой буфер - структура данных, в которой за последним элементом следует первый.
Также у этой структуры данных обязательно есть фиксированный предельный размер
FIFO - first in, first out. Это модель взаимодействия с кольцевым буфером по типу очереди.
Ниже представлены две реализации: на основе списка и дека.
Первая реализация лучше читается и короче, но по скорости записи и чтения они одинаковы.
"""

class CircularDeque:
    def __init__(self, capacity):
        self.size = capacity
        self.buffer = deque(maxlen=capacity)

    def append(self, item):
        self.buffer.append(item)

    def get(self):
        return list(self.buffer)

    def __repr__(self):
        return f"CircularDeque({self.get()})"

class CircularList:
    def __init__(self, capacity):
        self.size = capacity
        self.buffer = [None] * capacity
        self.head = 0
        self.tail = 0
        self.count = 0

    def append(self, item):
        self.buffer[self.tail] = item
        self.tail = (self.tail + 1) % self.size

        if self.count < self.size:
            self.count += 1
        else:
            self.head = (self.head + 1) % self.size

    def get(self):
        if self.count == 0:
            raise IndexError("Buffer is empty")
        items = []
        for i in range(self.count):
            index = (self.head + i) % self.size
            items.append(self.buffer[index])
        return items

    def __repr__(self):
        return f"CircularBuffer({self.get()})"

"""
существует много методов сортировки, основные из них делятся на устойчивые и неустойчивые.
timsort реализована в python в методе sort, сложность алгоритма в лучшем случае O(1), в худшем O(logN*N).
С точки зрения скорости алгоритма это лучший алгоритм сортировки,
он эффективней сортировки слиянием(в лучшем случае О(N)), и намного эффективней быстрой сортировки(O(NlogN) в лучшем, O(N^2) в худшем).
При этом алгоритм требует много памяти, но в задаче говорилось о тиках процессора, поэтому, в данном случае,
требуется именно алгоритмическая сложность.
"""
def binary_search(arr, item, start, end):
    if start == end:
        if arr[start] > item:
            return start
        else:
            return start + 1
    if start > end:
        return start

    middle = round((start + end)/ 2)

    if arr[middle] < item:
        return binary_search(arr, item, middle + 1, end)

    elif arr[middle] > item:
        return binary_search(arr, item, start, middle - 1)

    else:
        return middle

def insertion_sort(arr):
    l = len(arr)
    for index in range(1, l):
        value = arr[index]
        pos = binary_search(arr, value, 0, index - 1)
        arr = arr[:pos] + [value] + arr[pos:index] + arr[index+1:]
    return arr

def merge(left, right):
    """
    функция, которая возвращает отсортированный массив слитый из двух сортированных массивов
    О(n)
    """
    if not left:
        return right
    if not right:
        return left
    if left[0] < right[0]:
        return [left[0]] + merge(left[1:], right)
    return [right[0]] + merge(left, right[1:])

def timsort(arr):
    runs = []
    sorted_runs = []
    length = len(arr)
    new_run = [arr[0]]

    for i in range(1, length):
        # если i это последний элемент
        if i == length - 1:
            new_run.append(arr[i])
            runs.append(new_run)
            break
        if arr[i] < arr[i-1]:
            if not new_run:
                runs.append([arr[i]])
                new_run.append(arr[i])
            else:
                runs.append(new_run)
                new_run = []
        else:
            new_run.append(arr[i])
    # сортировка вставками для каждого элемента проходки
    for item in runs:
        sorted_runs.append(insertion_sort(item))

    # слияние отсортированных проходок
    sorted_array = []
    for run in sorted_runs:
        sorted_array = merge(sorted_array, run)

    print(sorted_array)
    return sorted_array

timsort([2, 3, 1, 5, 6, 7])
