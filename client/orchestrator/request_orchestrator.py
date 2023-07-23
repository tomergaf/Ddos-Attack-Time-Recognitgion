import math
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor
import requests
from client.client_config import *
from server.logging import logger as log

logger = log.logger

ALPHABET = string.ascii_uppercase

def send_request(payload):
    url = f'http://{HOSTNAME}:{PORT}/{ENDPOINT}'
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error sending request with payload: {payload}")
        print(e)


def run():
    logger.log("Initiating senders")
    thread_pool = ThreadPoolExecutor(max_workers=5)
    payloads_arr = []
    attack_payload_arr = []
    results = []

     # init payloads
    for _ in range(PAYLOAD_AMOUNT):
        payloads_arr.append(generate_random_payload())

    destination = random.choice(ALPHABET)
    for _ in range(ATTACKER_PAYLOAD_AMOUNT):
        attack_payload_arr.append(generate_attacker_payload(destination))

    _run_friendly(payloads_arr, thread_pool, results, TIME_SEC)
    _run_attack(attack_payload_arr, thread_pool, results, destination)
    _run_friendly(payloads_arr, thread_pool, results, TIME_SEC*1.5)

    list(results)
    thread_pool.shutdown(wait=True)

def _run_friendly(payloads_arr, thread_pool, results, time_to_run):
    logger.log("start friendly")
    for i in range(0, math.ceil(time_to_run)):
        results += thread_pool.map(send_request, payloads_arr)
        time.sleep(1)
    logger.log("finish friendly")

def _run_attack(attack_payload_arr, thread_pool, results, destination):
    logger.log("start attack")
    results += thread_pool.map(send_request, [{'source': random.choice(ALPHABET), 'destination': destination, 'type': 'AttackInit'}])
    results += thread_pool.map(send_request, attack_payload_arr)
    results += thread_pool.map(send_request, [{'source': random.choice(ALPHABET), 'destination': destination, 'type': 'AttackFinished'}])

def generate_random_payload():
    return {
        'source': random.choice(ALPHABET),
        'destination': random.choice(ALPHABET),
        'type': random.choice(ALPHABET)
    }

def generate_attacker_payload(destination: str):
    return {
        'source': random.choice(ALPHABET),
        'destination': destination,
        'type': destination
    }


if __name__ == '__main__':
    run()