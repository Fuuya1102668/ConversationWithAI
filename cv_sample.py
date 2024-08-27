import cv2

# 動画ファイルのパス
video_path = "dottimo.mp4"

# ウィンドウの名前
window_name = 'Video Player'

# 動画キャプチャの設定
cap = cv2.VideoCapture(video_path)

# 動画ファイルのフレームレートを取得
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Video FPS: {fps}")

# フレーム間の遅延を計算
delay = int(1000 / fps)

# ウィンドウの作成
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 動画の再生ループ
while True:
    ret, frame = cap.read()
    if not ret:
        break  # 動画の最後まで再生したらループを終了
    
    cv2.imshow(window_name, frame)

    # 遅延の設定
    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break  # 'q'キーが押されたら再生を停止

# ウィンドウを閉じる
cap.release()
cv2.destroyAllWindows()

