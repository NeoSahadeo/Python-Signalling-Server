from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# In-memory storage for demonstration purposes
saved_urls = []


@app.route('/save_url', methods=['POST'])
def save_url():
    # Capture the request URL
    url = request.json.get('url')
    if url:
        saved_urls.append(url)
        return jsonify({"message": "URL saved successfully!"}), 200
    return jsonify({"error": "No URL provided!"}), 400


@app.route('/send_info', methods=['POST'])
def send_info():
    # Example data to send
    data = {"message": "Hello, this is your information!"}

    for url in saved_urls:
        try:
            # Send data back to the saved URL
            response = requests.post(url, json=data)
            print(f"Sent to {url}: {response.status_code}")
        except Exception as e:
            print(f"Failed to send to {url}: {e}")

    return jsonify({"message": "Information sent to all saved URLs!"}), 200


if __name__ == '__main__':
    app.run()  # Use 'adhoc' for self-signed SSL
