import psutil
import serial
import time
import clr
import sys
import socket
import requests  # Thêm thư viện requests để lấy vị trí từ IP công cộng

sys.path.append(r"C:\OpenHardwareMonitor")  # Đường dẫn đến DLL
clr.AddReference("OpenHardwareMonitorLib")
from OpenHardwareMonitor import Hardware

ser = serial.Serial('COM8', 9600)
time.sleep(1)

computer = Hardware.Computer()
computer.GPUEnabled = True
computer.Open()

# === Hàm lấy dữ liệu phần cứng ===
def get_gpu_info():
    for hw in computer.Hardware:
        if hw.HardwareType in [Hardware.HardwareType.GpuNvidia, Hardware.HardwareType.GpuAti]:
            hw.Update()
            temp = load = None
            for sensor in hw.Sensors:
                if sensor.SensorType == Hardware.SensorType.Temperature and "GPU Core" in sensor.Name:
                    temp = f"{sensor.Value:.0f}'C"
                if sensor.SensorType == Hardware.SensorType.Load and "GPU Core" in sensor.Name:
                    load = f"{sensor.Value:.0f}%"
            return load or "N/A", temp or "N/A"
    return "N/A", "N/A"

def get_cpu_info():
    return f"{psutil.cpu_percent(interval=None):.1f}%" 

def get_ram_info():
    return f"{psutil.virtual_memory().percent:.0f}%" 

def get_net_speed(prev, now):
    download = (now.bytes_recv - prev.bytes_recv) / 1024 / 1024
    upload = (now.bytes_sent - prev.bytes_sent) / 1024 / 1024
    return f"Down:{download:.1f} Up:{upload:.1f}"

# Hàm lấy thông tin ổ đĩa và hiển thị nó với format cần thiết cho LCD 20x4
def get_disks_info():
    disk_info = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        free_space = usage.free / (1024 * 1024 * 1024)  # GB
        total_space = usage.total / (1024 * 1024 * 1024)  # GB
        disk_info.append(f"{free_space:.0f}/{total_space:.0f}")
    
    return disk_info

# Hàm lấy thông tin Wi-Fi và IP
def get_wifi_info():
    wifi_info = {}
    try:
        # Kiểm tra kết nối Wi-Fi
        wifi_status = "Connected" if psutil.net_if_stats().get('Wi-Fi', None) and psutil.net_if_stats()['Wi-Fi'].isup else "Not Connected"
        local_ip = socket.gethostbyname(socket.gethostname())  # IP nội bộ
        wifi_info['wifi_status'] = wifi_status
        wifi_info['local_ip'] = local_ip
    except Exception as e:
        wifi_info['wifi_status'] = "Error"
        wifi_info['local_ip'] = "N/A"
    
    return wifi_info

def get_location_info():
    try:
        response = requests.get("http://ipinfo.io/json")  # Lấy thông tin IP công cộng từ ipinfo.io
        data = response.json()
        location =  data.get('country', 'Unknown')
        ip = data.get('ip', 'N/A')
        return ip, location
    except requests.RequestException:
        return  "N/A"
    
# Gửi dữ liệu nếu có thay đổi
last_sent_message = ""

def send_to_lcd(message):
    global last_sent_message
    if message != last_sent_message:
        ser.write((message + '\n').encode())
        last_sent_message = message

# Biến điều khiển
update_interval = 1
prev_net = psutil.net_io_counters()
last_update_time = 0
page = 1
last_switch_time = time.time()

# Vòng lặp chính
while True:
    current_time = time.time()

    if current_time - last_update_time >= update_interval:
        last_update_time = current_time

        if page == 1:
            cpu_load = get_cpu_info()
            ram = get_ram_info()
            gpu_load, gpu_temp = get_gpu_info()
            current_net = psutil.net_io_counters()
            net_info = get_net_speed(prev_net, current_net)
            prev_net = current_net

            line1 = "Computer Lyner:"
            line2 = f"CPU:{cpu_load}  RAM:{ram}"
            line3 = f"GPU:{gpu_load} TEMP:{gpu_temp}"
            line4 = net_info

            full_message = f"{line1}|{line2}|{line3}|{line4}"
            print("[Trang 1]", full_message)
            send_to_lcd(full_message)

        elif page == 2:
            detail = "Computer info| CPU: i5-12400F| RAM: 32GB| GPU: RX 6600"
            print("[Trang 2]", detail)
            send_to_lcd(detail)

        elif page == 3:
            # Trang 3: Thông tin ổ cứng (toàn bộ ổ đĩa)
            disk_info = get_disks_info()

            # Hiển thị thông tin ổ đĩa lên LCD
            # Dòng 2: C:169/282   D:69/238
            # Dòng 3: E:62/238   F:98/195
            line1  = "Disk info:"
            line2 = f"C:{disk_info[0]} D:{disk_info[1]}" 
            line3 = f"E:{disk_info[2]}  F:{disk_info[3]}"

            # In ra để kiểm tra trên console
            full_message = f"{line1}| {line2}| {line3}"
            print("[Trang 3]", full_message)
            send_to_lcd(full_message)

        elif page == 4:
            # Trang 4: Thông tin Wi-Fi và IP
            wifi_info = get_wifi_info()
            public_ip, location = get_location_info()

            line1 = f"Network:"
            line2 = f"Wi-Fi:{wifi_info['wifi_status']}"
            line3 = f"IP:{wifi_info['local_ip']}"
            line4 = f"Loc:{location}"
            # In ra để kiểm tra trên console
            full_message = f"{line1}| {line2}| {line3}| {line4}"
            print("[Trang 4]", full_message)
            send_to_lcd(full_message)

    # Luân phiên trang
    if page == 1 and current_time - last_switch_time >= 10:
        page = 2
        last_switch_time = current_time
    elif page == 2 and current_time - last_switch_time >= 1:
        page = 3
        last_switch_time = current_time
    elif page == 3 and current_time - last_switch_time >= 4:
        page = 4
        last_switch_time = current_time
    elif page == 4 and current_time - last_switch_time >= 4:
        page = 1
        last_switch_time = current_time
