import base64
from flask import Flask, request, render_template_string

app = Flask(__name__)

def xor_bytes(data: bytes, key: bytes) -> bytes:
    """Performs XOR directly on raw bytes."""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

UI_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>secure message tool by skyro Softman</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f9; padding: 20px; max-width: 600px; margin: auto; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
        input[type="text"], textarea { width: 100%; padding: 10px; margin: 8px 0 15px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { background: #007bff; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { background: #e9ecef; padding: 10px; border-radius: 4px; word-break: break-all; margin-top: 10px; }
    </style>
</head>
<body>
    <h2>Secure Message Cipher Tool</h2>

    <div class="card">
        <h3>Encrypt Message</h3>
        <form method="POST" action="/encrypt-web">
            <label>Message / Text:</label>
            <textarea name="message" rows="3" required>{{ enc_msg }}</textarea>
            
            <label>key:</label>
            <input type="password" name="password" value="{{ enc_pass }}" required>
            
            <button type="submit">Encrypt</button>
        </form>
        {% if enc_result %}
            <p><strong>Result (Ciphertext):</strong></p>
            <div class="result">{{ enc_result }}</div>
        {% endif %}
    </div>

    <div class="card">
        <h3>Decrypt Message</h3>
        <form method="POST" action="/decrypt-web">
            <label>Ciphertext:</label>
            <textarea name="ciphertext" rows="3" required>{{ dec_cipher }}</textarea>
            
            <label>key:</label>
            <input type="password" name="password" value="{{ dec_pass }}" required>
            
            <button type="submit">Decrypt</button>
        </form>
        {% if dec_result %}
            <p><strong>Result (Original Message):</strong></p>
            <div class="result">{{ dec_result }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(UI_HTML)

@app.route('/encrypt-web', methods=['POST'])
def web_encrypt():
    message = request.form.get('message', '')
    key = request.form.get('password', '')
    try:
        encrypted_bytes = xor_bytes(message.encode('utf-8'), passcode.encode('utf-8'))
        ciphertext = base64.b64encode(encrypted_bytes).decode('utf-8')
        return render_template_string(UI_HTML, enc_result=ciphertext, enc_msg=message, enc_pass=passcode)
    except Exception as e:
        return render_template_string(UI_HTML, enc_result=f"Error: {str(e)}", enc_msg=message, enc_pass=passcode)

@app.route('/decrypt-web', methods=['POST'])
def web_decrypt():
    ciphertext = request.form.get('ciphertext', '')
    key = request.form.get('password', '')
    try:
        encrypted_bytes = base64.b64decode(ciphertext.encode('utf-8'))
        decrypted_bytes = xor_bytes(encrypted_bytes, passcode.encode('utf-8'))
        original_message = decrypted_bytes.decode('utf-8')
        return render_template_string(UI_HTML, dec_result=original_message, dec_cipher=ciphertext, dec_pass=passcode)
    except Exception:
        return render_template_string(UI_HTML, dec_result="Decryption failed! Invalid ciphertext or wrong passcode.", dec_cipher=ciphertext, dec_pass=passcode)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
