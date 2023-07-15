from datetime import datetime
import math
from collections import defaultdict
import matplotlib.pyplot as plt


class DataProcessing:
    def __init__(self, logger):
        self.payloads = []
        self.index = 0
        self.logger = logger

    def register_payload(self, source, destination, payload_type):
        payload = {
            'source': source,
            'destination': destination,
            'type': payload_type,
            'index': self.index,
            'time': datetime.now()
        }
        self.index += 1
        self.payloads.append(payload)

    def process_payloads_periodically(self, processing_function, interval_seconds):
        import time

        while True:
            for payload in self.payloads:
                processing_function(payload)

            time.sleep(interval_seconds)

    def calculate_entropy(self, start_index, end_index, resolution):
        sample_size = math.ceil((end_index - start_index + 1) / resolution)
        frequencies = defaultdict(int)

        # Count the frequency of each payload type and source-destination pair within the specified range and resolution
        for i in range(start_index, end_index + 1, resolution):
            if i < len(self.payloads):
                payload = self.payloads[i]
                payload_type = payload['type']
                source = payload['source']
                destination = payload['destination']
                key = (payload_type, source, destination)
                frequencies[key] += 1

        # Calculate the probability of each payload type and source-destination pair
        probabilities = [count / sample_size for count in frequencies.values()]

        # Calculate the entropy
        entropy = -sum(p * math.log2(p) for p in probabilities if p != 0)

        # Normalize the entropy according to the sample size
        normalized_entropy = entropy / math.log2(len(frequencies)) if len(frequencies) > 1 else 0

        l2_normalized_entropy = normalized_entropy * math.sqrt(len(frequencies))

        return l2_normalized_entropy

        # return normalized_entropy

    def calculate_entropy_over_period(self, start_index, max_end_index, resolution, parameter='time'):
        max_end_index = min(max_end_index, self.index)
        end_indices = range(start_index, max_end_index, resolution)  # Adjusted range

        entropy_values = []
        measurements = []
        indices = []

        # Iterate over element in resolution sized intervals
        for end_index in end_indices:
            entropy = self.calculate_entropy(start_index, end_index, resolution)
            entropy_values.append(entropy)
            print(f' len is {len(self.payloads)} curr index is {end_index}')
            measurements.append(self.payloads[end_index][parameter])
            indices.append(end_index)
        return measurements, entropy_values, indices

    def plot_entropy(self,start_index, max_end_index, resolution, service_type):
        if service_type == 'time':
            self.plot_entropy_over_time(start_index, max_end_index, resolution)
            pass
        elif service_type == 'index':
            self.plot_entropy_over_indices(start_index, max_end_index, resolution)
            pass

    def plot_entropy_over_time(self, start_index, max_end_index, resolution):

        (timestamps, entropy_values, indices) = self.calculate_entropy_over_period(start_index, max_end_index, resolution, 'time')

        # Plot the entropy values over time

        plt.plot(timestamps, entropy_values)
        plt.xlabel('Time')
        plt.ylabel('Entropy')
        plt.title('Entropy over Time')
        plt.show()

    def plot_entropy_over_indices(self, start_index, max_end_index, resolution):
        (timestamps, entropy_values, indices) = self.calculate_entropy_over_period(start_index, max_end_index,
                                                                                   resolution, 'index')

        # Plot the entropy values over time

        plt.plot(indices, entropy_values)
        plt.xlabel('Indices')
        plt.ylabel('Entropy')
        plt.title('Entropy over Indices')
        plt.show()

    def plot_attack_time(self):
        for payload in self.payloads:
            if payload['type'] == 'AttackInit':
                plt.axvline(x=payload['index'], color='r', linestyle='--', label='AttackInit')

        plt.legend()
        plt.show()

    def plot_detected_attack_window(self, start_index, end_index):
        plt.axvline(x=self.payloads[start_index]['index'], color='g', linestyle='--', label='Detected Start L')
        plt.axvline(x=self.payloads[end_index]['index'], color='b', linestyle='--', label='Detected Start R')

        plt.legend()
        plt.show()
