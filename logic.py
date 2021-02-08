import time
import urllib
import concurrent.futures
from collections import OrderedDict
from datetime import datetime, timedelta


class LogsProcessing():
    response_data = dict()
    
    @staticmethod
    def get_log_key(data):
        log_time = datetime.utcfromtimestamp(
                int(data[1])/1000
        ).replace(microsecond=0)

        log_time_range_start = log_time - timedelta(
            minutes=log_time.minute%15,
            seconds=log_time.second
        )
        log_time_range_end = log_time_range_start + timedelta(
            minutes=15
        )

        range_start = log_time_range_start.strftime("%H:%M")
        range_end = log_time_range_end.strftime("%H:%M")
        
        return dict(
            formatted_time=range_start + "-" + range_end,
            log_time_range_start=log_time_range_start
        )


    @staticmethod
    def aggregation_logic(file_link):
        file = urllib.request.urlopen(file_link)

        for line in file:
            decoded_line = line.decode("utf-8").splitlines()
            data = decoded_line[0].split(" ")

            log_keys = LogsProcessing.get_log_key(data)
            log_time_nearest_formatted = log_keys["formatted_time"]
            log_time_range_start = log_keys["log_time_range_start"]
            
            if log_time_range_start in LogsProcessing.response_data:
                entry_exists = LogsProcessing.response_data[log_time_range_start]
                exception_exists = [
                    exception_entry
                    for exception_entry in entry_exists["logs"]
                    if exception_entry["exception"] == data[2]
                ]
                if len(exception_exists):
                    exception_exists[0]["count"] += 1
                else:
                    current_exception = {
                        "exception": data[2],
                        "count": 1
                    }
                    entry_exists["logs"].append(current_exception)
                    entry_exists["logs"] = sorted(
                        entry_exists["logs"],
                        key = lambda i: i['exception']
                    )
            else:
                exception_log = {
                    "exception": data[2],
                    "count": 1
                }
                current_entry = {
                    "timestamp": log_time_nearest_formatted,
                    "logs": [exception_log]
                }
                LogsProcessing.response_data[log_time_range_start] = current_entry


    @staticmethod
    def process_logs_logic(log_files, max_workers):
        result = []        
        start = time.perf_counter()

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(LogsProcessing.aggregation_logic, log_files)
        
        ordered_data = OrderedDict(
            sorted(LogsProcessing.response_data.items(), 
            key=lambda t: t[0])
        )

        result = [ordered_data[key] for key in ordered_data]
        LogsProcessing.response_data.clear()

        end = time.perf_counter()
        print(f"Execution Time: {round(end-start, 2)}")
        
        return result
