import os
import sys
import requests
from threading import Thread
from multiprocessing import Pool
import aiohttp
import asyncio
import time
import argparse


def read_urls_from_file(file_path):
    """Чтение URL-адресов из файла."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")

    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]

    if not urls:
        raise ValueError("No URLs found in the file.")

    return urls


# Многопоточный подход
class ImageDownloader(Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        start_time = time.time()
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Проверка успешности запроса
            file_name = os.path.basename(self.url)
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Thread: {file_name} downloaded in {time.time() - start_time:.2f} seconds")
        except requests.RequestException as e:
            print(f"Thread: Error downloading {self.url}: {e}")


def threaded_download(urls):
    print("Starting threaded download...")
    threads = [ImageDownloader(url) for url in urls]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("Threaded download completed.")


# Многопроцессорный подход
def download_image(url):
    start_time = time.time()
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка успешности запроса
        file_name = os.path.basename(url)
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Process: {file_name} downloaded in {time.time() - start_time:.2f} seconds")
    except requests.RequestException as e:
        print(f"Process: Error downloading {url}: {e}")


def multiprocessing_download(urls):
    print("Starting multiprocessing download...")
    with Pool() as pool:
        pool.map(download_image, urls)
    print("Multiprocessing download completed.")


# Асинхронный подход
async def download_image_async(session, url):
    start_time = time.time()
    try:
        async with session.get(url) as response:
            response.raise_for_status()  # Проверка успешности запроса
            file_name = os.path.basename(url)
            with open(file_name, 'wb') as file:
                file.write(await response.read())
        print(f"Async: {file_name} downloaded in {time.time() - start_time:.2f} seconds")
    except aiohttp.ClientError as e:
        print(f"Async: Error downloading {url}: {e}")


async def async_download(urls):
    print("Starting async download...")
    async with aiohttp.ClientSession() as session:
        tasks = [download_image_async(session, url) for url in urls]
        await asyncio.gather(*tasks)
    print("Async download completed.")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != '--method':
        print("Usage: python download_images.py --method {threading,multiprocessing,asyncio}")
        sys.exit(1)

    method = sys.argv[2]
    if method not in ['threading', 'multiprocessing', 'asyncio']:
        print("Invalid method. Choose from 'threading', 'multiprocessing', 'asyncio'.")
        sys.exit(1)

    try:
        urls = read_urls_from_file('images.txt')
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    start_time = time.time()

    if method == 'threading':
        threaded_download(urls)
    elif method == 'multiprocessing':
        multiprocessing_download(urls)
    elif method == 'asyncio':
        asyncio.run(async_download(urls))

    print(f"Total time ({method}): {time.time() - start_time:.2f} seconds")
