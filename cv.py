import cv2
import socket
import time

# 動画ファイルのパス
video1 = "taiki01.mp4" # 入力待機
video2 = "kaitou.mp4" # 回答時

# ウィンドウの名前
window_name = 'Video Player'

# UDPソケットの設定
UDP_IP = "127.0.0.1"
UDP_PORT = 23456
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# 初期動画を設定
current_video = video1

# ウィンドウの作成
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 動画キャプチャの設定
cap = cv2.VideoCapture(current_video)
fps = cap.get(cv2.CAP_PROP_FPS)
delay = int(1000 / fps)  # フレーム間の遅延

# UDPソケットの非ブロッキング設定
sock.setblocking(False)

while True:
    ret, frame = cap.read()
    if not ret:
        cap.release()
        cap = cv2.VideoCapture(current_video)
        continue  # 動画が終了したら最初から再生

    cv2.imshow(window_name, frame)

    # 非ブロッキングでUDPパケットをチェック
    try:
        data, addr = sock.recvfrom(1024)  # データを受信
        data = data.decode('utf-8').strip()
        if data == 'video1':
            current_video = video1
            cap.release()
            cap = cv2.VideoCapture(current_video)
        elif data == 'video2':
            current_video = video2
            cap.release()
            cap = cv2.VideoCapture(current_video)
    except BlockingIOError:
        pass  # データが届いていない場合はスルー

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break  # 'q'キーが押されたら終了

# クリーンアップ
cap.release()
cv2.destroyAllWindows()
sock.close()

