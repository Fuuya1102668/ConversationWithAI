import cv2
import socket
import time

# 動画ファイルのパス
video1 = "dottimo.mp4"
video2 = "kutipaku.mp4"

# ウィンドウの名前
window_name = 'Video Player'

# 動画キャプチャの設定
cap = cv2.VideoCapture(video1)

# 動画ファイルのフレームレートを取得
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Video FPS: {fps}")

# フレーム間の遅延を計算
delay = int(1000/fps)

# UDPソケットの設定
UDP_IP = "127.0.0.1"  # サーバーのIPアドレス
UDP_PORT = 23456      # 受信側のポート番号
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# 初期動画を設定
current_video = video1

# ウィンドウの作成
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:  # 無限ループで再生
    cap = cv2.VideoCapture(current_video)
    if not cap.isOpened():
        print(f"Error opening video file: {current_video}")
        break
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 動画の最後まで再生したらループを抜ける（再度最初から再生）

        cv2.imshow(window_name, frame)
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break  # 'q'キーが押されたら再生を停止

        # 非ブロッキングでUDPパケットをチェック
        sock.settimeout(1.0)
        try:
            data, addr = sock.recvfrom(1024)  # 1024バイトのデータを受信
            data = data.decode('utf-8').strip()
            if data == 'video1':
                current_video = video1
                break  # 内側のループを抜けて動画を切り替える
            elif data == 'video2':
                current_video = video2
                break  # 内側のループを抜けて動画を切り替える
        except socket.timeout:
            continue

    cap.release()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # 'q'キーが押されたら無限ループを終了

# ウィンドウを閉じる
cv2.destroyAllWindows()

