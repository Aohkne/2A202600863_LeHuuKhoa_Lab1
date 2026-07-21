# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Ở temperature 0.0, model gần như luôn trả về cùng một sự thật (thường là những thông tin phổ biến nhất, ví dụ về Vịnh Hạ Long hoặc phở) — phản hồi ổn định, dễ đoán và ít lỗi diễn đạt. Khi tăng lên 0.5–1.0, các sự thật được đưa ra đa dạng hơn, câu văn tự nhiên và "sáng tạo" hơn nhưng vẫn giữ được tính chính xác. Ở 1.5, phản hồi bắt đầu lan man, đôi khi lặp từ hoặc pha trộn thông tin không liên quan, cho thấy độ ngẫu nhiên cao làm giảm độ mạch lạc và độ tin cậy của nội dung.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Khoảng 0.0–0.3. Chatbot hỗ trợ khách hàng cần trả lời nhất quán, chính xác và bám sát chính sách/quy trình của công ty - nhiệt độ thấp giúp giảm rủi ro model "sáng tạo" ra thông tin sai (hallucination) hoặc trả lời khác nhau cho cùng một câu hỏi giữa các lần gọi, điều rất quan trọng để giữ uy tín và tính chuyên nghiệp.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Tổng token/ngày = 10.000 × 3 × 350 = 10.500.000 token = 10.500 nghìn token.
> - Chi phí GPT-4o: 10.500 × $0.010 = **$105/ngày**
> - Chi phí GPT-4o-mini: 10.500 × $0.0006 = **$6.30/ngày**
>
> GPT-4o đắt hơn GPT-4o-mini khoảng **16.7 lần** (0.010 / 0.0006), tương đương chênh lệch ~$98.70/ngày, hay ~$2.960/tháng (30 ngày) cho cùng một workload.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> GPT-4o xứng đáng cho các tác vụ đòi hỏi suy luận phức tạp, độ chính xác cao và ngữ cảnh dài — ví dụ hệ thống trợ lý pháp lý phân tích hợp đồng, hoặc công cụ sinh/review code, nơi một câu trả lời sai lệch có thể gây thiệt hại lớn hơn nhiều so với phần chi phí chênh lệch. Ngược lại, GPT-4o-mini phù hợp hơn cho các tác vụ đơn giản, khối lượng lớn — ví dụ phân loại intent của tin nhắn, trả lời FAQ cơ bản, hay tóm tắt ngắn — nơi độ chính xác "đủ tốt" và tốc độ/chi phí thấp quan trọng hơn khả năng suy luận sâu.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng nhất trong các ứng dụng tương tác trực tiếp với người dùng — như chatbot hoặc trợ lý ảo — nơi độ trễ cảm nhận (perceived latency) ảnh hưởng lớn đến trải nghiệm: người dùng thấy chữ xuất hiện ngay lập tức thay vì phải chờ vài giây nhìn màn hình trống, tạo cảm giác hệ thống "đang suy nghĩ" và phản hồi nhanh hơn thực tế. Ngược lại, non-streaming phù hợp hơn khi ứng dụng cần xử lý toàn bộ phản hồi như một khối hoàn chỉnh trước khi dùng — ví dụ khi output là JSON có cấu trúc cần parse, khi kết quả được dùng trong pipeline tự động (không có người xem trực tiếp), hoặc khi cần kiểm duyệt/validate nội dung trước khi hiển thị cho người dùng.


## Danh Sách Kiểm Tra Nộp Bài
- [x] Tất cả tests pass: `pytest tests/ -v`
- [x] `call_openai` đã triển khai và kiểm thử
- [x] `call_openai_mini` đã triển khai và kiểm thử
- [x] `compare_models` đã triển khai và kiểm thử
- [x] `streaming_chatbot` đã triển khai và kiểm thử
- [x] `retry_with_backoff` đã triển khai và kiểm thử
- [x] `batch_compare` đã triển khai và kiểm thử
- [x] `format_comparison_table` đã triển khai và kiểm thử
- [x] `exercises.md` đã điền đầy đủ
- [x] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
