# Lab 3: Áp dụng thuật toán DES vào Truyền thông Socket

## 1. Giới thiệu
Bài thực hành này tập trung vào việc ứng dụng thuật toán bảo mật phân lớp Data Encryption Standard (DES) để bảo mật đường truyền thông tin giữa hai tiến trình thông qua cơ chế mạng (Socket Programming). 
Thông qua mô hình Client - Server đơn giản, chúng ta sẽ mô phỏng cách hai thiết bị (Sender và Receiver) giao tiếp và bảo vệ dữ liệu khỏi việc bị nghe lén (Eavesdropping).

## 2. Mục tiêu
- Hiểu và triển khai được mô hình truyền thông Socket cơ bản (TCP) bằng Python hoặc ngôn ngữ lập trình tương đương.
- Áp dụng thuật toán mã hóa khối (Block Cipher) DES vào việc mã hóa thông điệp thực tế.
- Xử lý các vấn đề thực tiễn khi dùng mã hoá khối, ví dụ như đệm dữ liệu (Padding) do DES yêu cầu dữ liệu đầu vào phải luôn là bội số của 64 bit (8 bytes).

## 3. Kiến trúc hệ thống & Phân công
Hệ thống bao gồm các thành phần chính trực thuộc thư mục dự án:
- **Sender (`sender.py` - Đinh Quang Huy)**: Đóng vai trò là Client. Chạy trên một tiến trình chờ người dùng nhập tin nhắn, đệm dữ liệu (padding) cho đúng kích thước, mã hóa bằng khóa bí mật DES và gửi đoạn dữ liệu đã mã hóa (Ciphertext) qua Socket.
- **Receiver (`receiver.py` - Nguyễn Đức Lâm)**: Đóng vai trò là Server. Lắng nghe các kết nối qua cổng TCP, nhận Ciphertext từ Sender, tiến hành giải mã (decryption) bằng cùng khóa DES, loại bỏ phần đệm (Unpadding) và hiển thị văn bản gốc (Plaintext).
- **Tiện ích (`des_socket_utils.py`)**: Thư viện chứa các hàm hỗ trợ đóng gói (padding/unpadding với chuẩn PKCS#7), các gói tin và quản lý header mạng cơ bản để truyền tải an toàn.

## 4. Cơ chế hoạt động
Quy trình gửi nhận dữ liệu diễn ra theo các bước sau:
1. **Thiết lập kết nối**: Khởi chạy `receiver.py` để mở một cổng (port) cục bộ và sẵn sàng lắng nghe. Khởi chạy `sender.py` để thực hiện kết nối tới địa chỉ IP và port của Receiver.
2. **Xử lý thông điệp (phía Sender)**:
   - Thông điệp người dùng dạng văn bản (String) được chuyển đổi thành chuỗi byte.
   - Bổ sung đệm dữ liệu (Padding) để đảm bảo độ dài (số byte) chia hết cho 8.
   - Thực hiện mã hóa luồng byte này qua thuật toán DES cùng một Khóa bí mật (Symmetric Key) quy định trước.
   - Truyền dữ liệu cipher qua đường kết nối Socket TCP.
3. **Nhận và giải mã (phía Receiver)**:
   - Đọc các gói dữ liệu từ Socket.
   - Đưa dữ liệu qua hàm giải mã của DES bằng Khóa bí mật tương ứng.
   - Bỏ các byte dư thừa ở đuôi (Unpadding) để khôi phục chính xác thông điệp gốc dài/ngắn tuỳ ý.
   - Hiển thị văn bản (Plaintext) ra màn hình console.

## 5. Đặc điểm và rủi ro bảo mật (Threat Model)
- **Tấn công vét cạn (Brute-force):** Thuật toán DES cơ bản với kích thước khóa thực tế 56-bit hiện nay có thể bị bẻ khóa bằng kỹ thuật dùng sức mạnh phần cứng. Do đó, hiện nay người ta thường dùng AES hoặc Triple DES.
- **Lưu trữ khóa:** Trong bài lab, do tính chất minh hoạ, khóa bí mật có thể đang được cấu hình tĩnh (hard-code) giữa hai bên. Trong thực tế, cần tích hợp nền tảng trao đổi khóa công khai mã hóa tự động để đảm bảo tính sinh đôi khóa an toàn (VD: Diffie-Hellman).
- **Không có toàn vẹn dữ liệu (Data Integrity):** DES chỉ đảm bảo tính bí mật (Confidentiality) mà chưa có cơ chế kiểm tra (MAC / HMAC) để biết dữ liệu có bị kẻ xấu (Man-in-the-middle) cố tình thay đổi giữa đường đi hay không (nếu dùng chế độ ECB hay CBC không kèm MAC). Đây là điểm cần lưu ý khi xây dựng ứng dụng thật.