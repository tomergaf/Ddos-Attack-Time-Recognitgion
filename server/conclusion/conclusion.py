from server.server_config import *

class ConclusionUnit:
    def __init__(self, data_processing_unit, end_index, resolution, threshold):
        self.data_processing_unit = data_processing_unit
        self.resolution = resolution  # Initial resolution
        self.start_index = resolution*2
        self.end_index = end_index
        self.threshold = threshold  # Threshold for entropy spike detection
        self.conclusion = "placeholder"

    def calculate_entropy(self):
        entropy = self.data_processing_unit.calculate_entropy_over_period(self.start_index, self.end_index, self.resolution)
        return entropy

    def detect_entropy_spike(self, timestamps, entropy_values, indices):
        max_spike = 0
        spike_index = 0
        for i in range(1, len(entropy_values)):
            curr_spike = abs(entropy_values[i] - entropy_values[i - 1]) if i>1 else 0
            if curr_spike >= self.threshold and curr_spike>max_spike and indices[i] > START_CHECKING_FROM:  #curr_spike < MAX_SPIKE_POSSIBLE:
                max_spike = curr_spike
                spike_index = i
                start_timestamp = timestamps[i - 1]
                end_timestamp = timestamps[i]
                self.data_processing_unit.logger.log(f'Entropy spike detected between {start_timestamp} - index {indices[spike_index-1]} and {end_timestamp} - index {indices[spike_index]}')

        if max_spike > 0:
            self.start_index = indices[spike_index-2] if spike_index>2 else indices[spike_index-1]
            self.end_index = indices[spike_index]
            should_stop = self.request_finer_dataset()
            self.data_processing_unit.logger.log("Reducing resolution")
            self.conclusion = f'Maximum Spike is between index {self.start_index} and {self.end_index} - between {start_timestamp} and {end_timestamp} '
            return should_stop
        return True

    def request_finer_dataset(self):
        # Adjust resolution to a finer level
        self.resolution //= 2  # For example, halve the resolution
        self.data_processing_unit.logger.log(f'Resolution is now {self.resolution}, Continuing')
        if self.resolution < 1:
            self.resolution = 1  # Minimum resolution of 1
            return True
        return False

    def process_entropy_data(self, entropy):
        timestamps, entropy_values, indices = entropy
        return self.detect_entropy_spike(timestamps, entropy_values, indices)

    def trigger_processing(self, plot):
        # Entrypoint
        should_stop = False
        while not should_stop:
            entropy = self.calculate_entropy()
            should_stop = self.process_entropy_data(entropy)
        if plot:
            self.data_processing_unit.plot_detected_attack_window(self.start_index, self.end_index)
        self.data_processing_unit.logger.log(f'Calculation done, conclusion is: {self.conclusion}')
        return self.conclusion


