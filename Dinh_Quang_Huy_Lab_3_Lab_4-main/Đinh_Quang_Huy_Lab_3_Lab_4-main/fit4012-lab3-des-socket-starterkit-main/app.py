from flask import Flask, render_template, request, jsonify
import socket
import os
from des_socket_utils import encrypt_des_cbc, build_packet

app = Flask(__name__)

SERVER_IP = os.getenv('SERVER_IP', '127.0.0.1')
# Khôi phục cổng 6000 gốc để gửi thẳng vào file receiver.py cổ điển
SERVER_PORT = int(os.getenv('SERVER_PORT', '6000')) 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message', '')
    if not message:
        return jsonify({'status': 'error', 'message': 'Vui lòng nhập tin nhắn'}), 400
    
    try:
        # Encode message
        plain_bytes = message.encode('utf-8')
        
        # Mã hóa (DES-CBC)
        key, iv, ciphertext = encrypt_des_cbc(plain_bytes)
        
        # Đóng gói tin (build_packet)
        packet = build_packet(key, iv, ciphertext)
        
        # Gửi qua socket TCP tới Receiver gốc (Cổng 6000)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(packet)
            
        # Trả về kết quả mã hóa để hiển thị lên Web
        return jsonify({
            'status': 'success',
            'key_hex': key.hex(),
            'iv_hex': iv.hex(),
            'ciphertext_hex': ciphertext.hex(),
            'packet_len': len(packet),
            'log': 'Đã bắn 1 gói TCP thẳng vào cổng 6000!'
        })
        
    except ConnectionRefusedError:
        return jsonify({
            'status': 'error', 
            'message': f'Lỗi kết nối gốc: Tiến trình Receiver.py (cổng {SERVER_PORT}) hiện chưa mở. Cần bật file receiver.py lên trước!'
        }), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("🚀 URL MÁY GỬI SENDER (WEB GUI): http://127.0.0.1:5000")
    print("Vui lòng đảm bảo rằng bạn đã chạy 'python receiver.py' ở Terminal gốc để chờ kết nối nha!")
    app.run(debug=True, port=5000)
