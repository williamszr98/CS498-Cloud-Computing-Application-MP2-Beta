from flask import Flask, jsonify
import subprocess
import socket
from multiprocessing import Process
import os

app = Flask(__name__)

def run_stress_cpu():
    """Run stress_cpu.py in a separate process"""
    try:
        subprocess.Popen(['python3', 'stress_cpu.py'])
    except Exception as e:
        print(f"Error running stress_cpu: {str(e)}")

@app.route("/", methods=["POST"])
def stress_cpu_handler():
    """Handle POST requests to trigger CPU stress"""
    try:
        # Start stress process in background
        Process(target=run_stress_cpu).start()
        return jsonify({"status": "CPU stress started"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def get_private_ip():
    """Handle GET requests to return private IP"""
    try:
        private_ip = socket.gethostbyname(socket.gethostname())
        return jsonify({"private_ip": private_ip}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)