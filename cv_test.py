import socket
import time

# 送信先のIPアドレスとポート番号
UDP_IP = "127.0.0.1"
UDP_PORT = 23456

sleep_time = 3

# UDPソケットの作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 1秒間隔でメッセージを送信
try:
    while True:
        sock.sendto(b"video1", (UDP_IP, UDP_PORT))
        time.sleep(sleep_time)
        sock.sendto(b"video2", (UDP_IP, UDP_PORT))
        time.sleep(sleep_time)
except KeyboardInterrupt:
    print("Program interrupted.")

finally:
    sock.close()

