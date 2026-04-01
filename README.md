cat << 'EOF' > README.md
# 🍎 BloxFruit Stock Notifier
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0%2B-blueviolet.svg)](https://discordpy.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Một công cụ tự động hóa mạnh mẽ giúp theo dõi kho trái ác quỷ (Stock) trong Blox Fruit. Bot tự động quét API và gửi thông báo trực tiếp đến Discord thông qua Webhook ngay khi **Normal Shop** hoặc **Mirage Island** có đợt làm mới (Reset).

## ✨ Tính năng nổi bật

* 🔄 **Theo dõi song song:** Giám sát đồng thời cả `Normal Stock` và `Mirage Stock` trong thời gian thực[cite: 1].
* 🚀 **Phát hiện Reset thông minh:** Sử dụng cơ chế *Fingerprint Signature* để nhận diện thay đổi kho hàng chính xác, tránh gửi thông báo trùng lặp[cite: 1].
* 📱 **Giao diện Webhook hiện đại:** Sử dụng các thành phần UI cao cấp của Discord như `LayoutView`, `Containers`, và `Separators` để tạo thông báo trực quan[cite: 1].
* ⏰ **Trình thời gian thực:** Hiển thị chính xác thời gian còn lại cho đến lần Reset tiếp theo của cả hai kho hàng[cite: 1].
* 💎 **Tự động Highlight:** Tự động tìm kiếm và làm nổi bật trái ác quỷ có giá trị cao nhất (`price_beli`) kèm hình ảnh minh họa[cite: 1].
* 🛠️ **Độ ổn định cao:** Tích hợp trình quản lý lỗi (Error Logging) và cơ chế tự động thử lại để duy trì hoạt động 24/7[cite: 1].

## 🛠️ Yêu cầu hệ thống

* **Python:** Phiên bản 3.8 trở lên.
* **Thư viện:** `discord.py`, `aiohttp`, `flask`[cite: 1].

## 🚀 Hướng dẫn cài đặt nhanh

### 1. Cài đặt môi trường
Sao chép mã nguồn và cài đặt các thư viện cần thiết:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. Cấu hình Webhook
Mở tệp \`main.py\` và cập nhật URL Webhook Discord của bạn tại biến \`WEBHOOK_URL\`[cite: 1].

### 3. Khởi chạy
Chạy Bot bằng lệnh:
\`\`\`bash
python main.py
\`\`\`

## 📊 Cấu trúc thông báo Webhook

* **Header:** Hiển thị sự kiện (Khởi động, Mirage Reset, hoặc Normal Reset) kèm tên nhà cung cấp[cite: 1].
* **Stock List:** Danh sách tên trái cây và giá tiền (\`Beli\`) được định dạng rõ ràng[cite: 1].
* **Footer:** Ghi chú tự động cập nhật và nút liên kết đến Server hỗ trợ[cite: 1].

## 🤝 Đóng góp & Hỗ trợ
* **Support Server:** [Gia nhập Discord](https://discord.gg/Zg2XkS5hq9)[cite: 1].
* **API Provider:** Dữ liệu được cung cấp bởi \`test-hub.kys.gay\`[cite: 1].

---
*Dự án được phát triển nhằm mục đích hỗ trợ cộng đồng người chơi Blox Fruit.*
EOF
