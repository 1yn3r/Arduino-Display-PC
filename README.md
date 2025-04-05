# System Monitor Display với Arduino Mega 2560 + LCD 20x4

## Mô tả dự án

Dự án này giúp hiển thị thông tin hệ thống máy tính lên **LCD 20x4** thông qua **Arduino Mega 2560**. Dữ liệu được lấy từ máy tính bằng Python và truyền qua cổng **Serial** đến Arduino.

Hệ thống hiển thị **luân phiên 4 trang thông tin** như sau:

---

## Trang 1: Thông tin hệ thống

Hiển thị các thông tin cơ bản về hiệu suất hệ thống:

- Tên máy: `Computer Lyner`
- CPU Load (%)
- RAM Usage (%)
- GPU Load (%) và nhiệt độ (°C)
- Tốc độ mạng: Download và Upload (MB/s)

**Ví dụ hiển thị:**
Computer Lyner: CPU:22% RAM:46% GPU:35% TEMP:52'C Down:1.2 Up:0.3
---

## Trang 2: Cấu hình phần cứng

Hiển thị cấu hình phần cứng chính của máy:

- CPU: Tên model CPU
- RAM: Tổng dung lượng RAM
- GPU: Model card đồ họa

**Ví dụ hiển thị:**
Computer info CPU: i5-12400F RAM: 32GB GPU: RX 6600

---

## Trang 3: Thông tin ổ đĩa

Hiển thị dung lượng trống và tổng dung lượng của các ổ đĩa:

- Dòng 2: Ổ đĩa C, D
- Dòng 3: Ổ đĩa E, F

**Ví dụ hiển thị:**
Disk info: C:169/282 D:69/238 E:62/238 F:98/195

---

## Trang 4: Mạng & vị trí

Hiển thị thông tin mạng LAN hoặc Wi-Fi và địa chỉ IP:

- Trạng thái kết nối Wi-Fi (hoặc LAN)
- IP nội bộ (Local IP)
- IP công cộng (Public IP)
- Vị trí địa lý (city, country)

**Ví dụ hiển thị:**
Wi-Fi: Connected IP: 192.168.1.10 Loc: Ho Chi Minh, VN

---

## Công nghệ sử dụng

- **Python**: Thu thập dữ liệu hệ thống với `psutil`, `socket`, `requests` và `OpenHardwareMonitorLib`
- **Arduino**: Nhận dữ liệu từ Serial và hiển thị lên LCD 20x4 qua I2C
- **LCD 20x4**: Hiển thị dữ liệu theo từng trang
- **Cổng Serial (COMx)**: Giao tiếp giữa PC và Arduino Mega 2560

---

## Yêu cầu hệ thống

- Máy tính Windows
- Python 3.x và các thư viện:
  - `psutil`
  - `requests`
  - `pythonnet` (sử dụng `clr`)
- `OpenHardwareMonitorLib.dll` đặt tại thư mục `C:\OpenHardwareMonitor`
- Arduino Mega 2560 + LCD I2C 20x4
- Arduino IDE (để nạp chương trình cho Mega)

---
