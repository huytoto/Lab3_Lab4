# Report 1 page - Lab 3

## Thông tin nhóm
- Thành viên 1: TODO_STUDENT
- Thành viên 2: TODO_STUDENT

## Mục tiêu
TODO_STUDENT: Viết 4-6 dòng mô tả mục tiêu của bài lab.

## Phân công thực hiện
TODO_STUDENT: Mô tả ai phụ trách sender, ai phụ trách receiver, ai phụ trách test/log/threat model, và phần làm chung.

## Mô tả Quy trình 
Q1:
1. **Receiver.py** là chương trình mở cổng (gọi `.bind()` và `.listen()`) và chờ kết nối.
2. **Sender.py** là chương trình chủ động kết nối tới bộ nhận (gọi qua `.connect()`).
3. Gói tin được thiết kế và truyền đi tuần tự theo thứ tự: **Key (8 bytes) -> IV (8 bytes) -> Length Header (4 bytes) -> Ciphertext (Mã hóa)**.
4. **Vai trò PKCS#7:** DES là thuật toán mã hóa Block Cipher yêu cầu đầu vào chia hết cho 8-byte. PKCS#7 làm nhiệm vụ chèn/bù thêm số lượng byte còn thiếu vào phần chuỗi cuối trước khi mã hóa (ví dụ thiếu 3 byte, nó chèn 3 byte có giá trị `0x03`). Khi giải mã, hệ thống đọc byte cuối để cắt gọt ngược lại.

## Kết quả
TODO_STUDENT: Chèn thêm Hình ảnh Terminal chạy thành công và các log chạy. Tóm tắt các test.

## Kết luận
Qua những bài thực hành test case lỗi từ Header, Truncated length, Tamper.. nhóm hiểu được rủi ro của việc tin tưởng đầu vào mù quáng. Cần bổ sung Try/Catch, Timeout socket và kiểm tra padding chặt chẽ. Đưa Plain text Key lên mạng là sai lầm bảo mật hệ thống nghiêm trọng nhất.
