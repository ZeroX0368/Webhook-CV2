# 🍎 BloxFruit Stock Notifier
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0%2B-blueviolet.svg)](https://discordpy.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Một công cụ tự động hóa mạnh mẽ giúp theo dõi kho trái ác quỷ (Stock) trong Blox Fruit. Bot tự động quét API và gửi thông báo trực tiếp đến Discord thông qua Webhook ngay khi **Normal Shop** hoặc **Mirage Island** có đợt làm mới (Reset).

## ✨ Tính năng nổi bật

* 🔄 **Theo dõi song song:** Giám sát đồng thời cả `Normal Stock` và `Mirage Stock` trong thời gian thực.
* 🚀 **Phát hiện Reset thông minh:** Sử dụng cơ chế *Fingerprint Signature* để nhận diện thay đổi kho hàng chính xác, tránh gửi thông báo trùng lặp.
* 📱 **Giao diện Webhook hiện đại:** Sử dụng các thành phần UI cao cấp của Discord như `LayoutView`, `Containers`, và `Separators` để tạo thông báo trực quan.
* ⏰ **Trình thời gian thực:** Hiển thị chính xác thời gian còn lại cho đến lần Reset tiếp theo của cả hai kho hàng.
* 💎 **Tự động Highlight:** Tự động tìm kiếm và làm nổi bật trái ác quỷ có giá trị cao nhất (`price_beli`) kèm hình ảnh minh họa.
* 🛠️ **Độ ổn định cao:** Tích hợp trình quản lý lỗi (Error Logging) và cơ chế tự động thử lại để duy trì hoạt động 24/7

## 🛠️ Yêu cầu hệ thống

* **Python:** Phiên bản 3.8 trở lên.
* **Thư viện:** `discord.py`, `aiohttp`

## 🚀 Hướng dẫn cài đặt nhanh

### 1. Cài đặt môi trường
Sao chép mã nguồn và cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### 3. Khởi chạy
Chạy Bot bằng lệnh:
```bash
python main.py
```
