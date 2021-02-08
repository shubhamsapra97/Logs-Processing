# Logs Processing

PROJECT START STEPS:

    Pre-requisites:
    1. Install need python and pip to be installed in your system.

    Steps:
    1. To run this application, do the following:
        1.a. Go to the project root directory.
        1.b. Run the following commands to install dependencies of the app:
        	- pip install -r requirements.txt
        1.c. Run the following command(s) in the terminal/command line to run the app:
            - python restapi.py
    
    2. Go to http://localhost:8080 in your browser to view it.

# Implementation:

- Project exposes a rest endpoint `POST - /api/process-logs/`
- Request data should contain following
    - logFiles: list of text files (publically available urls) containing logs in format
        - request_id  UTC_timestamp  Log_Exception_Namw
        - Example: 1  1612783483  NullPointerException
    - parallelFileProcessingCount: number of files to be processed in parallel
- Api aggregates the data using `parallelFileProcessingCount` number of threads in    parallel and reducing the processing time to less than half.

# Aggregation logic
- Based on the timestamp retrieved from log file, find the time range of the log
- time range is 15min window enclosing the log
- Eg: log creation time is: 31st Dec 2020 03:12:00
- `Time range` will be 03:00-03:15
- Logs are aggregated based on this time range and if multiple logs occur in a time range, they are sorted 
- Eg: `NullPointerException` and `AnyOtherException` exceptions were logged in same time range window. So in logs array `AnyOtherException` will come before `NullPointerException`. Refer to below structure for more.

- Respose Structure:
```
{
    "response": [
        {
            "timestamp": "time_range",
            "logs": [
                {
                    "exception": AnyOtherException,
                    "count": 1
                },
                {
                    "exception": NullPointerException,
                    "count": 5
                }
            ]
        }
    ]
}
```
