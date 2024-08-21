import cv2
import threading
import time

# 動画ファイルのパス
video1 = "kutipaku.mp4"
video2 = "dottimo.mp4"

# ウィンドウの名前
window_name1 = 'Video 1'
window_name2 = 'Video 2'

# フレームレートを設定
fps = 30
delay = int(1000 / fps)

def display_video(video_path, window_name):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return
    
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(window_name, frame)
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyWindow(window_name)

# スレッドの作成
thread1 = threading.Thread(target=display_video, args=(video1, window_name1))
thread2 = threading.Thread(target=display_video, args=(video2, window_name2))

# スレッドの開始
thread1.start()
thread2.start()

# スレッドの終了を待機
thread1.join()
thread2.join()

print("Both videos have finished playing.")

