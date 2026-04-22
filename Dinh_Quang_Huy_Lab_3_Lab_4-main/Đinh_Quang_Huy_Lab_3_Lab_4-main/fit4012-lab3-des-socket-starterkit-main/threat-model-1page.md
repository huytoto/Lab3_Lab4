# Threat Model - Lab 3

## Thông tin nhóm
- Thành viên 1: TODO_STUDENT
- Thành viên 2: TODO_STUDENT

## Assets
- Plaintext của người dùng (bản rõ).
- Khóa DES 8-byte và IV.
- Log hệ thống lưu trữ giao dịch.
- Địa chỉ IP và cổng dịch vụ của Receiver.

## Attacker model
- Kẻ tấn công có thể nghe lén luồng mạng trong cùng mạng LAN (Sniffing).
- Kẻ tấn công có thể sửa đổi nội dung gói TCP trên đường truyền (Man-in-the-Middle).
- Kẻ tấn công chủ động gửi các luồng byte độc hại mạo danh vào socket.

## Threats
1. Lộ khóa vì gửi chung dưới dạng plaintext (Bắt được gói tin là có luôn chìa giải).
2. Sửa đổi ciphertext dẫn tới phá vỡ cấu trúc và lỗi giải mã tại receiver.
3. Chỉnh sửa độ dài mô tả trong gói (header) bị sai để chương trình đọc thiếu hoặc tràn.

## Mitigations
1. Không gửi key dạng plaintext, dùng cơ chế trao đổi khóa (Diffie-Hellman hoặc SSL/TLS).
2. Thêm MAC / HMAC để xác thực và tránh việc bị sửa đổi (tampering) trên đường truyền đi.
3. Đặt điều kiện ràng buộc giới hạn độ dài gói tin, đồng thời gắn kèm timeout và try/except.

## Residual risks
- Máy người dùng bị cài mã độc/trojan khiến tài sản gốc bị lộ ngay khi tải lên bộ nhớ RAM.
- Ghi log ra các file nhạy cảm mà những quy trình (process) khác có thể đọc được.
