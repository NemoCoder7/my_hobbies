import random

def randoms(min, max, n):
    return [random.randint(min, max) for _ in range(n)]


# for r in randoms(10, 30, 5):
#     print(r)

def random_generator(min, max, n):
    for i in range(n):
        yield random.randint(min, max)

# for r in random_generator(10, 30, 5):
#     print(r)
rand_seq = random_generator(1, 100, 5)
for r in rand_seq:
    print(r)


import itertools

rand_seq = random_generator(1, 100, 5)
five_taken = list(itertools.islice(rand_seq, 5))
print(five_taken)

