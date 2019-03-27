# Синхронный вариант.
# -------------------
# import requests
# from time import time


# def get_pic(url):
#     r = requests.get(url)
#     return r


# def write_file(response):
#     filename = response.url.split('/')[-1]
#     with open(filename, 'wb') as file:
#         file.write(response.content)


# def main():
#     url = 'https://loremflickr.com/320/240'

#     initial_time = time()

#     for i in range(10):
#         write_file(get_pic(url))

#     print(f'Прошло {time() - initial_time} сек.')


# if __name__ == "__main__":
#     main()


# Асинхронный вариант.
# --------------------
import asyncio
from time import time

import aiohttp


def write_image(data):
    filename = f'file-{int(time() * 1000)}.jpeg'
    with open(filename, 'wb') as file:
        file.write(data)


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        write_image(data)


async def main():
    url = 'https://loremflickr.com/320/240'

    tasks = []

    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    initial_time = time()
    asyncio.run(main())
    print(f'Прошло {time() - initial_time} сек.')
