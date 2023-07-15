import requests
import json
from client.client_config import *
from server.logging import logger as log
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
import time

logger = log.logger

def send_request(payload):
    url = 'http://{}:{}/{}'.format(HOSTNAME, PORT, ENDPOINT)
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        #print(f"Request sent successfully with payload: {payload}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error sending request with payload: {payload}")
        print(e)

def send_friendly(thread_pool, times):
    for elem in range(times):
        payloads = [
            {'source': 'A', 'destination': 'B', 'type': 'X'},
            {'source': 'C', 'destination': 'D', 'type': 'Y'},
            {'source': 'E', 'destination': 'F', 'type': 'Z'},
            {'source': 'G', 'destination': 'H', 'type': 'X'},
            {'source': 'I', 'destination': 'J', 'type': 'Y'}
        ]

        futures = []
        for payload in payloads:
            future = thread_pool.submit(send_request, payload)
            futures.append(future)
        # Wait for all tasks to complete
    # thread_pool.shutdown(wait=True)
    logger.log("Friendly done")
    return futures

def send_hostile(thread_pool, times):
    logger.log("Started attacking")
    payload = {'source': 'A', 'destination': 'B', 'type': 'AttackInit'}
    thread_pool.submit(send_request, payload)
    for elem in range(times):
        payloads = [
            {'source': 'A', 'destination': 'B', 'type': 'X'},
            {'source': 'C', 'destination': 'B', 'type': 'Y'},
            {'source': 'E', 'destination': 'B', 'type': 'Z'},
            {'source': 'G', 'destination': 'B', 'type': 'X'},
            {'source': 'I', 'destination': 'B', 'type': 'Y'}
        ]

        futures = []
        for payload in payloads:
            future = thread_pool.submit(send_request, payload)
            futures.append(future)

        # Wait for all tasks to complete
    thread_pool.shutdown(wait=True)
    logger.log("Done attacking")
    return futures

def main():
    # Create a thread pool with 5 threads
    futures = []
    logger.log("Initiating senders")
    thread_pool_friendly = ThreadPoolExecutor(max_workers=5)
    thread_pool_hostile = ThreadPoolExecutor(max_workers=5)

    friendly_futures = send_friendly(thread_pool_friendly, 10)
    time.sleep(ATTACK_DELAY)
    hostile_futures = send_hostile(thread_pool_hostile, 4)
    friendly_futures = send_friendly(thread_pool_friendly, 10)

    # Combine all the futures
    all_futures = friendly_futures + hostile_futures

    wait(all_futures)

    # Wait for all tasks to complete and process the results
    for future in as_completed(all_futures):
        result = future.result()
        # Process the result as needed
        logger.log(result.content)


    # futures.append(send_friendly(thread_pool_friendly, 5))
    # time.sleep(ATTACK_DELAY);
    # futures.append(send_hostile(thread_pool_hostile, 3))

    # Print the results
    # for future in futures:
    #     result = future.result()
    #     print(result.content)

if __name__ == '__main__':
    main()