import requests
import json
from client.client_config import *
from concurrent.futures import ThreadPoolExecutor

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


def main():
    # Create a thread pool with 5 threads
    thread_pool = ThreadPoolExecutor(max_workers=5)

    # Define the JSON payloads to send
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
    thread_pool.shutdown(wait=True)

    # Print the results
    for future in futures:
        result = future.result()
        print(result.content)

if __name__ == '__main__':
    main()