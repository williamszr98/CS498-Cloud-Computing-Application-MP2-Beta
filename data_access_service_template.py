from flask import Flask, request
import threading

# Global variables for the seed and lock
seed_value = 0
seed_lock = threading.Lock()

# App for handling GET requests on port 5000
app_get = Flask("GetApp")

@app_get.route("/", methods=["GET"])
def get_seed():
    with seed_lock:
        current_seed = seed_value
    return str(current_seed)

# App for handling POST requests on port 8080
app_post = Flask("PostApp")

@app_post.route("/", methods=["POST"])
def update_seed():
    data = request.get_json()
    new_num = data['num']
    with seed_lock:
        global seed_value
        seed_value = new_num
    return str(new_num)

def run_get_app():
    app_get.run(host='0.0.0.0', port=5000)

def run_post_app():
    app_post.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_get_app)
    t2 = threading.Thread(target=run_post_app)
    t1.start()
    t2.start()
    t1.join()
    t2.join()