from flask import Flask, request
from server.server_config import *

app = Flask(__name__)

@app.route('/')
def index():
    return 'Flask Server is running'

@app.route('/keepalive')
def keepalive():
    return 'Server is alive'\

@app.route('/send-message', methods=['POST'])
def registermessage():
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