import requests
import json
from time import time
import threading

lock = threading.Lock()


def retrieve_data(number):
    url = f"https://jsonplaceholder.typicode.com/posts/{number}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")


def write_response_to_json(data):
    with open("data.json", "r") as f:
        file_data = json.load(f)

    file_data.append(data)

    with open("data.json", "w") as f:
        json.dump(file_data, f)


def read_and_write_to_json(number):
    data = retrieve_data(number)
    lock.acquire()
    write_response_to_json(data)
    lock.release()


def main_sequential():
    start_time = time()
    with open("data.json", "w") as f:
        json.dump([], f)
    for i in range(1, 78):
        read_and_write_to_json(i)
    end_time = time()
    print(f"Total time: {end_time - start_time}")


def main_thread():
    start_time = time()
    with open("data.json", "w") as f:
        json.dump([], f)

    thread_list = []
    for i in range(1, 78):
        thread = threading.Thread(target=read_and_write_to_json, args=(i,))
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    end_time = time()
    print(f"Total time: {end_time - start_time}")


if __name__ == "__main__":
    # main_sequential()
    main_thread()
