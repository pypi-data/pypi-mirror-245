import atexit
import csv
from datetime import datetime
import os
import threading
import dateparser

from queue import Queue
import time


class Limiter():
    def __init__(self, client):
        self.client = client
        self.log_queue = Queue()
        self.stop = False

        # Start the logging thread
        logging_thread = threading.Thread(target=self.write_logs)
        logging_thread.daemon = True
        logging_thread.start()

        atexit.register(self._finish)

        # Set the thread's niceness to 19 (Unix-like systems only)
        try:
            os.nice(19)
        except AttributeError:
            # Handle the case where `os.nice` is not available (e.g., on Windows)
            pass

    def _finish(self):
        self.stop = True
        self._write()

    def _write(self):
        dir_path = f"output/{self.client.organization}"
        file_path = f"{dir_path}/requests.csv"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(file_path, mode='a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Empty the queue and write to the CSV
            while not self.log_queue.empty():
                log_entry = self.log_queue.get()
                csv_writer.writerow(
                    [log_entry['timestamp'], log_entry['endpoint']])

    def write_logs(self):
        while not self.stop:
            self._write()
            time.sleep(8)

    def lazy_log_request(self, endpoint):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log_queue.put({'timestamp': now, 'endpoint': endpoint})

    def cost(self, since="1970-01-01"):
        dir_path = f"output/{self.client.organization}"
        file_path = f"{dir_path}/requests.csv"

        if not os.path.exists(file_path):
            return "No requests made yet."

        count = 0
        since_date = dateparser.parse(since)

        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                timestamp_str, _ = row
                timestamp = datetime.strptime(
                    timestamp_str, '%Y-%m-%d %H:%M:%S')

                if timestamp > since_date:
                    count += 1

        return f"{count} requests since {since_date}"
