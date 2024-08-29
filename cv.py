import cv2
import time

# 動画ファイルのパス
video1 = "taiki01.mp4"  # 入力待機
video2 = "kaitou.mp4"  # 回答時

# ウィンドウの名前
window_name = 'Video Player'

# 初期動画を設定
current_video = video1

# ウィンドウの作成
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 動画キャプチャの設定
cap = cv2.VideoCapture(current_video)
fps = cap.get(cv2.CAP_PROP_FPS)
delay = int(1000 / fps)  # フレーム間の遅延

# フレームスキップの設定
frame_skip = 4  # 1フレームごとに表示（2なら2フレームに1回表示）

frame_count = 0

while True:
    start_time = time.time()  # フレーム読み込みの開始時間を記録

    ret, frame = cap.read()
    if not ret:
        cap.release()
        cap = cv2.VideoCapture(current_video)
        continue  # 動画が終了したら最初から再生
    frame_count += 1

    # フレームスキップ処理
    if frame_count % frame_skip == 0:
        cv2.imshow(window_name, frame)
    else:
        continue  # 動画が終了したら最初から再生


    end_time = time.time()  # フレーム読み込みの終了時間を記録
    print(f"Frame read time: {end_time - start_time:.4f} seconds")  # フレーム読み込み時間を表示

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break  # 'q'キーが押されたら終了

# クリーンアップ
cap.release()
cv2.destroyAllWindows()

