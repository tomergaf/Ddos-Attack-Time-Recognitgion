from flask import Flask, request
from server.server_config import *
from server.processing.data_processing import DataProcessing
from server.conclusion.conclusion import ConclusionUnit
from server.logging import logger as log
import logging
import threading


app = Flask(__name__)
logger = log.logger
processing_unit = DataProcessing(logger)


def calculate(resolution, max_requests, service_type, start_from):
    logger.log("Calculate Requested")
    processing_unit.plot_entropy(start_from, max_requests, resolution, service_type)

@app.route('/calculate')
def calculate_endpoint():
    resolution = int(request.args.get('resolution', 1))
    start_from = int(request.args.get('start', 0))
    max_requests = int(request.args.get('max_requests', 100))
    service_type = request.args.get('type', 'time')
    thread = threading.Thread(target=calculate, args=(resolution, max_requests, service_type, start_from))
    thread.start()
    return "Plotting graph in the background"

@app.route('/')
def index():
    logger.log("Server Started")
    return 'Flask Server is running'

@app.route('/keepalive')
def keepalive():
    return 'Server is alive'\

@app.route('/get-logs')
def get_logs():
    logger.log("Log Requested")
    return logger.get_logs()\

@app.route('/show-attack-time')
def show_attack_time():
    logger.log("Attack Time Requested")
    return processing_unit.plot_attack_time()\

@app.route('/find_spike')
def find_spike():
    logger.log("Conclusion Requested - Find Spike")
    resolution = int(request.args.get('resolution', DEFAULT_START_RESOLUTION))
    should_plot = bool(request.args.get('should_plot', False))
    conclusion_unit = ConclusionUnit(processing_unit, DEFAULT_END_INDEX, resolution, ATTACK_THRESHOLD)
    result = conclusion_unit.trigger_processing(should_plot)
    logger.log(result)
    return result \

@app.route('/send-message', methods=['POST'])
def register_message():
    """
    this gets the message, parses it, and stores it in the data processing unit

    """
    '''
    temp - will parse and print fields
    '''

    data = []
    payload = request.get_json()
    source = payload.get('source')
    destination = payload.get('destination')
    data_type = payload.get('type')

    processing_unit.register_payload(source, destination, data_type)

    logger.log(f"Payload registered - Source: {source}, Destination: {destination}, Type: {data_type}",logging.DEBUG)

    #DELETEME - for control and visibility
    data.append({
        'source': source,
        'destination': destination,
        'type': data_type
    })
    return 'Data stored successfully' + "\n" + print_data(data)

#TODO - DELETEME
def print_data(data):
    result = ''
    for item in data:
        result += f"Source: {item['source']}, Destination: {item['destination']}, Type: {item['type']}\n"
    return result

if __name__ == '__main__':
    app.run(port=PORT)