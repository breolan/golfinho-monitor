from flask import Flask, request, jsonify
import json
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask()

DATA_FILE = "data/network_data.json"

@app.route('/send_data', methods=['POST'])
def receive_data():
    try:
        data = request.json
        data["timestamp"] = datetime.now().isoformat()

        with open(DATA_FILE, "r+") as file:
            content = json.load(file)
            content.append(data)
            file.seek(0)
            json.dump(content, file, indent=4)

        return jsonify({"message": "Data received successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    try:
        with open(DATA_FILE, "r") as file:
            content = json.load(file)
        return jsonify(content), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

