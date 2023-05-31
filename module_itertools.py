import itertools as it

even_numb = [z for z in range(10) if z % 2 == 0]
print(even_numb)

even_numbers = it.count(0, 2)
print(even_numbers)

lst = list(next(even_numbers) for _ in range(5))
print(lst)

lst1 = list(zip(it.count(), ['a', 'b', 'c']))
print(lst1)

def print_iterable(iterable, end = None):
    for x in iterable:
        if end:
            print(x, end = end)
        else:
            print(x)


list(map(pow, range(10), it.repeat(2)))
pos_neg_ines = it.cycle([1, -1])
print(list(next(pos_neg_ines) for _ in range(10)))