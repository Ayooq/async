def initialize_coroutine(func):
    def inner(*args, **kwargs):
        coroutine = func(*args, **kwargs)
        coroutine.send(None)
        return coroutine
    return inner


def get_average():
    count = 0
    total = 0
    average = None

    while True:
        try:
            x = yield
        except StopIteration:
            break
        else:
            count += 1
            total += x
            average = round(total / count, 2)

    return average


@initialize_coroutine
def delegator(subgen):
    result = yield from subgen
    print('Среднее количество посетителей равняется', result)
