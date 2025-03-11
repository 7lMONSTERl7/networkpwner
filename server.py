from flask import Flask, request, jsonify, Response
import logging
import werkzeug
import queue
import sys
import os


sys.stdout = sys.stderr = open(os.devnull, 'w')
app = Flask(__name__)
app.logger.setLevel(logging.ERROR)

# Suppress werkzeug logs by changing the log level for werkzeug's logger
logging.getLogger('werkzeug').setLevel(logging.ERROR)
# Dictionary to store buffers for each device
device_buffers = {}

def get_client_ip(request):
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.remote_addr
    return ip


# Route to handle video frame uploads (POST)
@app.route('/upload_stream/', methods=['POST'])
def upload_stream():
    device_name = request.args.get('device_name')
    if not device_name:
        return jsonify({"error": "Missing device_name"}), 400

    if device_name not in device_buffers:
        device_buffers[device_name] = queue.Queue(maxsize=10)  # Increased buffer size

    try:
        # Capture the frame data
        frame_data = request.data

        # If buffer is full, discard the oldest frame
        if device_buffers[device_name].qsize() >= 10:
            device_buffers[device_name].get_nowait()

        # Add the frame to the buffer
        device_buffers[device_name].put(frame_data)

        return jsonify({"message": "Frame received"}), 200

    except queue.Full:
        return jsonify({"error": f"Buffer full for device: {device_name}"}), 429


# Route to stream video frames (GET)
@app.route('/stream/<device_name>/', methods=['GET'])
def stream(device_name):
    if device_name not in device_buffers:
        return jsonify({"error": "Device not found"}), 404

    def generate():
        buffer = device_buffers[device_name]
        while True:
            if not buffer.empty():
                frame_data = buffer.get()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

    return Response(generate(), content_type='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
