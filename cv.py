import cv2
import time

# 動画ファイルのパス
video1 = 'dottimo.mp4'
video2 = 'kutipaku.mp4'

# 再生間隔（秒）
play_duration = 3

# 動画キャプチャオブジェクトを作成
cap1 = cv2.VideoCapture(video1)
cap2 = cv2.VideoCapture(video2)

# ウィンドウの名前を指定
window_name = 'Video Player'

# フレームレートを設定
fps = 30
delay = int(1000 / fps)

# ウィンドウをフルスクリーンで表示する関数
def display_video(cap):
    global start_time
    start_time = time.time()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow(window_name, frame)
        
        # 一定時間経過後に映像を切り替え
        if time.time() - start_time > play_duration:
            break

        # 3秒ごとに映像を更新
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

# ウィンドウを作成し、動画を交互に表示するループ
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    # 最初の動画を表示
    cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 動画を最初に戻す
    display_video(cap1)

    # 次の動画を表示
    cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 動画を最初に戻す
    display_video(cap2)

    # ループを続けるか確認
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースを解放してウィンドウを閉じる
cap1.release()
cap2.release()
cv2.destroyAllWindows()

