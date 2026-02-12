# yield is used when we want to return a generator object from a function
# on demand instead of all at once.
# A generator function allows us to iterate over a sequence of values
# without storing them all in memory.
# On demand, the next value is produced when requested using the next()
# function or a loop.


def count_numbers(n):
    num = 1
    for _ in range(n):
        yield num
        num += 1


if __name__ == "__main__":
    # Using the generator function
    numbers = count_numbers(5)
    for number in numbers:
        print(number)
