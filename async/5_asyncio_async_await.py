import asyncio


async def print_nums():
    num = 1
    while True:
        print(num)
        num += 1
        await asyncio.sleep(0.2)


async def print_time():
    time = 0
    while True:
        if time % 3 == 0:
            print(f'Прошло {time} сек.')
        time += 1
        await asyncio.sleep(1)


async def main():
    task1 = asyncio.create_task(print_nums())
    task2 = asyncio.create_task(print_time())

    await asyncio.gather(task1, task2)


if __name__ == "__main__":
    asyncio.run(main())
