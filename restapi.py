import json
from flask import Flask, request, Response
from logic import LogsProcessing

app = Flask(__name__)


@app.route("/api/process-logs/", methods=["POST"])
def process_logs():
    result = []
    status_code = 200
    log_files = request.json["logFiles"]
    max_workers = request.json["parallelFileProcessingCount"]
    
    if not len(log_files) or max_workers <= 0:
        status_code = 400        
        result = dict(
            status="failure",
            reason="Parallel File Processing count must be greater than zero!"
        )
    else:
        processed_data = LogsProcessing.process_logs_logic(
            log_files,
            max_workers
        )
        result = dict(
            response=processed_data
        )

    return Response(
        json.dumps(result),
        status=status_code,
        content_type="application/json"
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
