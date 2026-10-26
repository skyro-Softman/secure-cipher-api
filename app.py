import base64
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

def xor_bytes(data: bytes, key: bytes) -> bytes:
    """Performs XOR directly on raw bytes."""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

HOME_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Secure Cipher API</title></head>
<body style="font-family: Arial; padding: 20px;">
    <h2>Secure Message Cipher API</h2>
    <p>Status: <b>Online 🚀</b></p>
    <p>Use endpoints: <code>/encrypt</code> or <code>/decrypt</code> using POST requests with JSON data.</p>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_PAGE)

@app.route('/encrypt', methods=['POST'])
def api_encrypt():
    data = request.get_json() or {}
    message = data.get('message', '')
    passcode = data.get('passcode', '')
    
    if not message or not passcode:
        return jsonify({"error": "Message and passcode are required"}), 400
        
    try:
        encrypted_bytes = xor_bytes(message.encode('utf-8'), passcode.encode('utf-8'))
        ciphertext = base64.b64encode(encrypted_bytes).decode('utf-8')
        return jsonify({"ciphertext": ciphertext})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def api_decrypt():
    data = request.get_json() or {}
    ciphertext = data.get('ciphertext', '')
    passcode = data.get('passcode', '')
    
    if not ciphertext or not passcode:
        return jsonify({"error": "Ciphertext and passcode are required"}), 400
        
    try:
        encrypted_bytes = base64.b64decode(ciphertext.encode('utf-8'))
        decrypted_bytes = xor_bytes(encrypted_bytes, passcode.encode('utf-8'))
        original_message = decrypted_bytes.decode('utf-8')
        return jsonify({"original_message": original_message})
    except Exception:
        return jsonify({"error": "Decryption failed! Invalid ciphertext or wrong password."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
