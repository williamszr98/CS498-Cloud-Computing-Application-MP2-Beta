from flask import Flask, request, jsonify
import requests
import json
import boto3

app = Flask(__name__)

# ===== CONFIGURATION =====
DATA_ACCESS_SERVICE_GET_URL = "http://3.80.227.73:5000/"  # REPLACE WITH ACTUAL IP
DATA_ACCESS_SERVICE_POST_URL = "http://3.80.227.73:8080/" # REPLACE WITH ACTUAL IP
NACL_ID = "acl-059d86675489fd38e"  # REPLACE WITH ACTUAL NACL ID
REGION = "us-east-1"          # UPDATE YOUR REGION
# =========================

ec2_client = boto3.client('ec2', region_name=REGION)

@app.route("/", methods=["GET"])
def route_get():
    try:
        # Get seed value from Data Access Service
        seed_response = requests.get(DATA_ACCESS_SERVICE_GET_URL)
        seed_value = seed_response.text.strip()
        
        # Get instance metadata
        token = requests.put(
            "http://169.254.169.254/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
            timeout=2
        ).text
        
        ip_response = requests.get(
            "http://169.254.169.254/latest/meta-data/public-ipv4",
            headers={"X-aws-ec2-metadata-token": token},
            timeout=2
        )
        public_ip = ip_response.text.strip()
        
        return jsonify({
            "seed": seed_value,
            "server_ip_address": public_ip
        }), 200
        
    except Exception as e:
        print(f"GET Error: {str(e)}")
        return "Error in processing request", 500

@app.route("/", methods=["POST"])
def route_post():
    try:
        # Forward update to Data Access Service
        data = request.get_json()
        update_response = requests.post(
            DATA_ACCESS_SERVICE_POST_URL,
            json=data,
            timeout=5
        )
        
        # Get NACL information
        nacl_response = ec2_client.describe_network_acls(
            NetworkAclIds=[NACL_ID]
        )
        
        return jsonify({nacl_response}), 200
        
    except Exception as e:
        print(f"POST Error: {str(e)}")
        return "Error in processing request", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)